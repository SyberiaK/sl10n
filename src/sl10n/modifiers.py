from __future__ import annotations
from typing import NamedTuple


class PreModifiers(NamedTuple):
    """
    Class that contains possible modifiers that would apply BEFORE locale processing.

    Available modifiers:

    - exclude (``bool``):
      Exclude file from parsing.
    """

    exclude: bool | None = None


class PostModifiers(NamedTuple):
    """
    Class that contains possible modifiers that would apply AT or AFTER locale processing.

    Available modifiers:

    - redump (``bool``):
      Redump file anyway.
    - lang_code (``str``):
      Override language code of translation file (it doesn't override the access key in ``SL10n.locale()``!).
    """

    redump: bool | None = None
    lang_code: str | None = None
