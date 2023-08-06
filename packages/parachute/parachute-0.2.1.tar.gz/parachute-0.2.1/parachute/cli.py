#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import TextIO

import click
import json5

from .craft_communication import CraftCommunication
from .data_types import Backup
from .data_types import Parameter
from .utils import RegexType


DEBUG = False


def debug(message: Any) -> None:
    """Print a message if DEBUG is True."""
    if DEBUG:
        click.echo(message)


def load_backup_from_file(backup_file: TextIO) -> Backup:
    """Load a list of parameters from a file."""
    data = json5.load(backup_file)
    return Backup.from_dict(data)


def save_backup_to_file(backup: Backup, outfile: TextIO) -> None:
    """Save a list of parameters to a file."""
    # Brace yourselves, we're going to perform some horrible hacks to
    # format the file for readability.

    # Write the status comment.
    outfile.write(backup.status_str)

    backup_dict = backup.as_dict()

    # Pop the parameters from the backup dict so we can write them later.
    parameters = backup_dict.pop("parameters")
    backup_dict["parameters"] = {}

    # Write the top-level backup.
    backup_str = json5.dumps(backup_dict, indent=2)

    param_str = "".join(
        (
            "    " + json5.dumps({name: data})[1:-1] + ",\n"
            for name, data in parameters.items()
        )
    )

    # Insert the param_str into the rest of the file and write it.
    outfile.write(backup_str[:-4] + "\n" + param_str + "  " + backup_str[-4:])


def read_backup_from_craft(socket: str) -> Backup:
    """Read all the parameters from a craft."""
    # From https://www.ardusub.com/developers/pymavlink.html.
    craft = CraftCommunication(socket)
    backup = Backup()
    param_generator = craft.list_params()
    backup.status = next(param_generator)  # type: ignore
    debug(backup.status)
    count = next(param_generator)
    for parameter in param_generator:
        debug(parameter)
        click.echo(f"- {str(parameter.index).rjust(4)} / {count}\r", nl=False)  # type: ignore
        backup.parameters[parameter.name] = parameter  # type: ignore
    return backup


@click.group()
@click.option("--debug", is_flag=True, help="Print debug information.")
def cli(debug):
    global DEBUG
    DEBUG = debug


@cli.command(help="Compare a previous backup to the parameters on a craft.")
@click.argument("backup_file", type=click.File("r"))
@click.option(
    "-s",
    "--socket",
    default="/dev/ttyACM0",
    show_default=True,
    help="Path to the USB socket.",
)
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
def compare(backup_file, socket, filter):
    click.echo("Comparing parameters...")
    craft = CraftCommunication(socket)
    backup = load_backup_from_file(backup_file)
    backup.filter(filter)
    all_parameters = set(backup.parameters.keys())
    seen_parameters = set()
    click.echo("Parameter name".ljust(24) + "Craft".rjust(24) + "Backup".rjust(24))
    click.echo("-" * (24 + 24 + 24))

    param_generator = craft.list_params()
    next(param_generator)
    count = next(param_generator)

    # Print parameters on the craft.
    for parameter in param_generator:
        # Ignore filtered parameters.
        click.echo(f"- {str(parameter.index).rjust(4)} / {count}\r", nl=False)
        if filter and not filter.search(parameter.name):
            continue

        if parameter.name in seen_parameters:
            # We've already seen this one.
            continue

        backup_value = (
            "-"
            if parameter.name not in all_parameters
            else backup.parameters[parameter.name].value
        )
        if parameter.value != backup_value:
            click.echo(
                parameter.name.ljust(24)
                + str(parameter.value).rjust(24)
                + str(backup_value).rjust(24)
            )
        seen_parameters.add(parameter.name)

    # Print parameters that were in the backup file but not the craft.
    for parameter_name in all_parameters - seen_parameters:
        click.echo(
            parameter_name.ljust(24)
            + "-".rjust(24)
            + str(backup.parameters[parameter_name].value).rjust(24)
        )

    # Print a long "Done" to erase any count.
    click.echo("Done.        ")


@cli.command(help="Restore a previous backup to a craft.")
@click.argument("backup_file", type=click.File("r"))
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.option(
    "-s",
    "--socket",
    default="/dev/ttyACM0",
    show_default=True,
    help="Path to the USB socket.",
)
def restore(backup_file, socket, filter):
    click.echo("Restoring parameters...")
    craft = CraftCommunication(socket)
    backup = load_backup_from_file(backup_file)
    backup.filter(filter)
    for name, parameter in backup.parameters.items():
        click.echo(f"Setting {parameter.name} = {parameter.value}...")
        craft.set_param(parameter)
    click.echo("Done.")


@cli.command(help="Back up all the parameters from a craft to a file.")
@click.argument("craft_name")
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.option(
    "-o",
    "--outdir",
    default=".",
    show_default=True,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="Directory to write the backup file to.",
)
@click.option(
    "-s",
    "--socket",
    default="/dev/ttyACM0",
    show_default=True,
    help="Path to the USB socket.",
)
def backup(craft_name, socket, outdir, filter):
    click.echo(f"Reading parameters from {socket}...")
    backup = read_backup_from_craft(socket)
    click.echo("Writing to file...")
    filename = Path(outdir) / (
        f"{craft_name}_" f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}" ".chute"
    )

    backup.filter(filter)

    # Write the actual backup.
    with filename.open("w") as outfile:
        save_backup_to_file(backup, outfile)
    click.echo("Done.")


@cli.command(help="Filter parameters by a regular expression.")
@click.argument("regex", type=RegexType())
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def filter(regex, backup_file, output_file):
    click.echo("Filtering based on regular expression...")
    backup = load_backup_from_file(backup_file)
    backup.filter(regex)
    save_backup_to_file(backup, output_file)
    click.echo("Done.")


@cli.command(name="get", help="Get and print parameters.")
@click.argument("params", nargs=-1)
@click.option(
    "-s",
    "--socket",
    default="/dev/ttyACM0",
    show_default=True,
    help="Path to the USB socket.",
)
def get_params(params, socket):
    click.echo("Retrieving parameters...")
    craft = CraftCommunication(socket)

    for param in params:
        param = craft.get_param(Parameter(name=param))
        click.echo(f"  {param.name} = {param.value}")


@cli.command(name="set", help="Set parameters.")
@click.argument("params", nargs=-1)
@click.option(
    "-s",
    "--socket",
    default="/dev/ttyACM0",
    show_default=True,
    help="Path to the USB socket.",
)
def set_params(params, socket):
    craft = CraftCommunication(socket)

    for param in params:
        if "=" not in param:
            click.echo(f"Wrong parameter syntax: {param} (should be NAME=VALUE).")
            continue

        name, value = param.split("=")
        parameter = Parameter(name=name, value=value)
        click.echo(f"Setting {parameter.name} = {parameter.value}...")
        craft.set_param(parameter)
    click.echo("Done.")


@cli.group(help="Convert a Parachute backup into another format.")
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.pass_context
def convert(ctx, filter):
    ctx.ensure_object(dict)

    ctx.obj["FILTER"] = filter


@convert.command(help='Convert into a QGroundControl ".params" file.')
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.pass_context
def qgc(ctx, backup_file, output_file):
    click.echo("Converting to a QGroundControl compatible file...")
    backup = load_backup_from_file(backup_file)
    backup.filter(ctx.obj["FILTER"])

    output_file.write("# Vehicle-Id Component-Id Name Value Type\n")
    output_file.writelines(
        f"1\t1\t{name}\t{parameter.value:.18g}\t{parameter.type}\n"
        for name, parameter in sorted(backup.parameters.items())
    )
    output_file.close()


@convert.command(help='Convert into a Mission Planner ".param" file.')
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.pass_context
def mp(ctx, backup_file, output_file):
    click.echo("Converting to a Mission Planner compatible file...")
    backup = load_backup_from_file(backup_file)
    backup.filter(ctx.obj["FILTER"])

    output_file.writelines(
        f"{name},{parameter.value}\n"
        for name, parameter in sorted(backup.parameters.items())
    )
    output_file.close()


if __name__ == "__main__":
    cli()
