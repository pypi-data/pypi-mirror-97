from dataclasses import dataclass
from typing import Collection


@dataclass(frozen=True)
class Logs:
    """Lines of logs."""

    lines: Collection[str]
    """Lines of logs."""

    def _repr_html_(self) -> str:
        return f"<pre>{str(self)}</pre>"

    def __str__(self) -> str:
        """Return the string representation."""
        return "".join(self.lines)
