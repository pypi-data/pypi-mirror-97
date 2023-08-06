from enum import Enum, auto


class Edition(Enum):
    """atoti edition."""

    COMMUNITY = auto()
    ENTERPRISE = auto()

    def __str__(self):
        """Return the edition string."""
        return str(self.name).lower()
