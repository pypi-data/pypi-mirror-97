from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, Mapping, Optional, Union

from ..exceptions import AtotiException
from ._utils import Configuration

Restrictions = Mapping[str, Union[str, Collection[str]]]
# Keep this collection up to date with the roles in SecurityConstants.java.
_SPECIAL_ROLES = ("ROLE_USER", "ROLE_ADMIN", "ROLE_ATOTI_ROOT", "ROLE_CS_ROOT")


@dataclass(frozen=True)
class Role(Configuration):
    """A role and its restrictions."""

    name: str
    restrictions: Restrictions

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_role(**data)


def create_role(name: str, *, restrictions: Optional[Restrictions] = None) -> Role:
    """Create a role with the given restrictions.

        * Restrictions apply on store columns and are inherited by all hierarchies based on these columns.
        * Restrictions on different hierarchies are intersected.
        * However, if a user has several roles with restrictions on the same hierarchies, the access to the union of restricted members will be granted.

    There are special roles in atoti that cannot be redefined:

        * ``ROLE_USER``: required to access the application.
        * ``ROLE_ADMIN``: gives full access (read, write, delete, etc...) to the application.

    Args:
        name: Role name.
        restrictions: Role restrictions.

    Example:
        >>> python_config = tt.config.create_config(
        ...     roles=[
        ...         tt.config.create_role(
        ...             "ROLE_AMERICA",
        ...             restrictions={"Country": ["Canada", "USA"]},
        ...         ),
        ...         tt.config.create_role(
        ...             "ROLE_CHINA", restrictions={"Country": "China"}
        ...         ),
        ...         tt.config.create_role(
        ...             "ROLE_FRANCE",
        ...             restrictions={"Country": "France", "Currency": "Euro"},
        ...         ),
        ...     ]
        ... )
        >>> yaml_config = '''
        ... roles:
        ...   - name: ROLE_AMERICA
        ...     restrictions:
        ...       Country: [Canada, USA]
        ...   - name: ROLE_CHINA
        ...     restrictions:
        ...       Country: China
        ...   - name: ROLE_FRANCE
        ...     restrictions:
        ...       Country: France
        ...       Currency: Euro
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

        In this example:

        * A user with the role ``ROLE_AMERICA`` will only see the data related to USA and Canada and will not see the data for France.
        * A user with the role ``ROLE_FRANCE`` will only see the data where the country is France AND the currency is Euro.
        * A user with both ``ROLE_AMERICA`` and ``ROLE_CHINA`` will see the data where the country is USA, Canada, OR China.

    """
    restr = dict()
    if restrictions is None:
        restrictions = dict()
    for key, value in restrictions.items():
        if not isinstance(value, list):
            restr[key] = [value]
    if name in _SPECIAL_ROLES:
        raise AtotiException(
            f"Role {name} is special and cannot be redefined, use another name."
        )
    return Role(name, restr)
