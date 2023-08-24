from __future__ import annotations
from typing import NamedTuple


class PreModifiers(NamedTuple):
    """
    Class that contains possible modifiers that activate BEFORE locale processing.

    This class is not intended to be inherited.

    Available modifiers:

    - exclude (``bool``):
      Exclude file from parsing.
    """

    exclude: bool | None = None


class PostModifiers(NamedTuple):
    """
    Class that contains possible modifiers that activate AT or AFTER locale processing.

    This class is not intended to be inherited.

    Available modifiers:

    - redump (``bool``):
      Redump file anyway.
    - lang_code (``str``):
      Override language code of translation file (it doesn't override the access key in ``SL10n.locale()``!).
    """

    redump: bool | None = None
    lang_code: str | None = None
