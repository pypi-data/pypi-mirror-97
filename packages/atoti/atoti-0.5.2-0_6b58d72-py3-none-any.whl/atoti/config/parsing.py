from typing import Any


class ConfigParsingError(ValueError):
    """Error raised when the parsing of the config failed."""

    def __init__(self, message: str, parsed_object: Any = None):
        """Create the parsing error.

        Args:
            message: The error message.
            parsed_object: The parsed object.

        """
        additional = "" if parsed_object is None else f"\n{str(parsed_object)}"
        super().__init__(f"{message}{additional}")
