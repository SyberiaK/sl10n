from typing import NamedTuple


class PreModifiers(NamedTuple):
    """
    Class that contains possible modifiers that activate BEFORE locale processing.

    This class is not intended to be inherited.

    Available modifiers:

    - exclude (``bool``): Exclude a file from parsing.
    """

    exclude: bool = None


class PostModifiers(NamedTuple):
    """
    Class that contains possible modifiers that activate AT or AFTER locale processing.

    This class is not intended to be inherited.

    Available modifiers:

    - redump (``bool``): Redump a file anyway.
    """

    redump: bool = None
