import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from textwrap import dedent
from typing import List

from ._edition import Edition
from ._path_utils import get_atoti_home
from ._version import VERSION

_EULA_PATH = Path(__file__).parent / "LICENSE"
COPIED_EULA_PATH = get_atoti_home() / "LICENSE"
HIDE_EULA_MESSAGE_ENV_VAR = "ATOTI_HIDE_EULA_MESSAGE"
EULA = _EULA_PATH.read_text(encoding="utf8") if _EULA_PATH.exists() else None


class OutputType(Enum):
    """Type of output."""

    EXCEPTION = auto()
    REGULAR = auto()
    WARNING = auto()


@dataclass(frozen=True)
class Output:
    """License-related output."""

    content: str
    output_type: OutputType


def hide_new_license_agreement_message():
    """Copy the current end-user license agreement to atoti's home directory."""
    if not EULA:
        raise Exception("This function can only be called in the community edition.")
    COPIED_EULA_PATH.write_text(EULA, encoding="utf8")


_EULA_OUTPUT = Output(
    f"""
    Welcome to atoti {VERSION}!

    By using this community edition, you agree with the license available at https://www.atoti.io/eula.
    Browse the official documentation at https://docs.atoti.io.
    Join the community at https://www.atoti.io/register.

    You can hide this message by setting the {HIDE_EULA_MESSAGE_ENV_VAR} environment variable to True.
    """,
    OutputType.REGULAR,
)

_EULA_CHANGED_OUTPUT = Output(
    f"""
    Thanks for updating to atoti {VERSION}!

    The license agreement has changed, it's available at https://www.atoti.io/eula.

    You can hide this message by calling `atoti.{hide_new_license_agreement_message.__name__}()`.
    """,
    OutputType.REGULAR,
)


def _has_eula_changed(copied_eula: str) -> bool:
    """Whether the EULA has changed (regardless of the version) since last import."""
    # Remove all the version occurences and whitespaces,
    # and put everything in lower case to minimize false positives
    previous, new = (
        re.sub(r"(\d+\.\d+\.\d+(\.\d+)?|\s)", "", text).lower()
        for text in (copied_eula, EULA or "")
    )
    return previous != new


def _log_about_eula(is_community_license: bool) -> List[Output]:
    outputs = []
    if is_community_license:
        if os.environ.get(HIDE_EULA_MESSAGE_ENV_VAR, "False").lower() == "true":
            if COPIED_EULA_PATH.exists():
                copied_eula = COPIED_EULA_PATH.read_text(encoding="utf8")
                if _has_eula_changed(copied_eula):
                    # License message was asked to be hidden through environment variable
                    # but the EULA has changed so we need to show it again.
                    outputs.append(_EULA_CHANGED_OUTPUT)
                elif copied_eula != (EULA or ""):
                    # If only the version has changed, just copy the new one.
                    hide_new_license_agreement_message()
            else:
                COPIED_EULA_PATH.parent.mkdir(parents=True, exist_ok=True)
                hide_new_license_agreement_message()
        else:
            outputs.append(_EULA_OUTPUT)

    return outputs


def _monitor_license_expiry(
    edition: Edition, end_date: datetime, is_community_license: bool
) -> List[Output]:
    outputs = []
    now = datetime.now()
    product_name = "atoti" if edition == Edition.COMMUNITY else "Atoti+"
    license_name = "atoti" if is_community_license else "Atoti+"
    # Community version can be used with an Atoti+ license: https://github.com/activeviam/atoti/issues/1907
    required_action = (
        "update to atoti's latest version or upgrade to Atoti+"
        if is_community_license
        else "contact ActiveViam to get a new license"
    )
    if end_date < now:
        outputs.append(
            Output(
                f"Your {license_name} license has expired, {required_action}.",
                OutputType.EXCEPTION,
            )
        )
    else:
        remaing_days = (end_date - now).days
        if remaing_days <= 7:
            outputs.append(
                Output(
                    f"""
                    Thanks for using {product_name} {VERSION}!

                    Your {license_name} license is about to expire, {required_action} in the coming {remaing_days} days.
                    """,
                    OutputType.WARNING,
                )
            )
    return outputs


def get_license_outputs(
    edition: Edition, end_date: datetime, is_community_license: bool
) -> List[Output]:
    """Generate list of outputs about the EULA and monitor license expiry."""
    outputs = _log_about_eula(is_community_license) + _monitor_license_expiry(
        edition, end_date, is_community_license
    )
    return [
        Output(dedent(output.content).strip(), output.output_type) for output in outputs
    ]


def check_license(edition: Edition, end_date: datetime, is_community_license: bool):
    """Log about the EULA and monitor license expiry."""
    for output in get_license_outputs(edition, end_date, is_community_license):
        if output.output_type == OutputType.EXCEPTION:
            raise Exception(output.content)
        if output.output_type == OutputType.REGULAR:
            print(output.content)
        elif output.output_type == OutputType.WARNING:
            logging.getLogger("atoti.licensing").warning(output.content)
