import re

import click


class RegexType(click.ParamType):
    name = "regex"

    def convert(self, value, param, ctx):
        try:
            return re.compile(value, re.IGNORECASE)
        except re.error as e:
            self.fail(
                "Regex error: " + str(e),
                param,
                ctx,
            )
