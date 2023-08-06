from typing import Generator
from typing import List
from typing import Union

from pymavlink import mavutil

from .data_types import Parameter


class CraftCommunication:
    def __init__(self, socket: str):
        self._conn = mavutil.mavlink_connection(socket)
        self._conn.wait_heartbeat()

    def get_param(self, parameter: Parameter) -> Parameter:
        """Retrieve a parameter from a craft."""
        # Request the parameter.
        self._conn.mav.param_request_read_send(
            self._conn.target_system,
            self._conn.target_component,
            parameter.name.encode(),
            -1,
        )

        # Wait for the response.
        while True:
            message = self._conn.recv_match(blocking=True).to_dict()
            if (
                message.get("mavpackettype", "") == "PARAM_VALUE"
                and message["param_id"] == parameter.name
            ):
                break
        return Parameter.from_message(message)

    def set_param(self, parameter: Parameter) -> None:
        """Set a parameter on a craft."""
        self._conn.mav.param_set_send(
            self._conn.target_system,
            self._conn.target_component,
            parameter.name.encode(),
            parameter.value,
            parameter.type,
        )

    def list_params(self) -> Generator[Union[List[str], int, Parameter], None, None]:
        """
        Read all the parameters from a craft.

        Yields the status as a list in first iteration, a count of all
        parameters in the second, and the parameters after that.
        """
        # From https://www.ardusub.com/developers/pymavlink.html.
        self._conn.mav.param_request_list_send(
            self._conn.target_system, self._conn.target_component, 1
        )
        status = []
        # This keeps track of the FSM state. If it's 0, we need to output the
        # status, 1 we need to output the count, and 2 is parameters until
        # we're done.
        fsm_state = 0
        while True:
            # Read all messages, as AP eventually freezes if we try to
            # ignore too many message types.
            message = self._conn.recv_match(blocking=True).to_dict()

            # The FC sends the status messages first and then starts sending
            # parameters, but it still might send unrelated status messages
            # after that. We're only interested in the first messages.
            if message.get("mavpackettype", "") == "STATUSTEXT" and fsm_state == 0:
                status.append(message["text"])
                continue
            elif message.get("mavpackettype", "") != "PARAM_VALUE":
                continue

            if fsm_state == 0:
                # We're done with status messages, yield the status.
                yield status
                fsm_state = 1
                continue
            elif fsm_state == 1:
                # This is the first parameter, yield the count and then the
                # parameter itself right away.
                yield message["param_count"]
                fsm_state = 2

            if message["param_id"].startswith("STAT_") or message["param_id"] in (
                "SYS_NUM_RESETS",
                "INS_GYROFFS_X",
                "INS_GYROFFS_Y",
                "INS_GYROFFS_Z",
            ):
                # Ignore statistical parameters.
                continue

            parameter = Parameter.from_message(message)
            yield parameter
            if parameter.index == message["param_count"] - 1:
                break
