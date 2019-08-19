"""Door serial interface."""

import serial

_OPEN_DOOR_COMMAND = b'o'
_RED_LED_COMMAND = b'n'


class DoorInterface:
    """Door interface."""

    def __init__(self, port: str = "/dev/ttyACM0") -> None:
        """Construct a DoorInterface."""
        self._port = serial.Serial(port, 9600)

    def get_card(self) -> str:
        """Wait until a card is presented, get ID."""
        return self._port.readline().decode("ascii").strip()  # type: ignore

    def open(self) -> None:
        """Open the door."""
        self._port.write(_OPEN_DOOR_COMMAND)

    def flash_red(self) -> None:
        """Flash the red LED."""
        self._port.write(_RED_LED_COMMAND)
