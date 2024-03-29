from __future__ import annotations


class DefaultLangFileNotFound(UserWarning):
    """Propogates when the default language file not found."""


class LangFileAlreadyExists(UserWarning):
    """Propogates when the language file already exists."""


class SL10nAlreadyInitialized(UserWarning):
    """Propogates when SL10n already initialized."""

    DEFAULT_MESSAGE = 'SL10n already initialized.'

    def __init__(self, message: str | None = None):
        self.message = message if message else self.DEFAULT_MESSAGE

    def __str__(self):
        return self.message


class UndefinedLocaleKey(UserWarning):
    """Propogates when found an undefined locale key."""


class UnexpectedLocaleKey(UserWarning):
    """Propogates when found an unexpected locale key."""


class UnfilledLocaleKey(UserWarning):
    """Propogates when found an unfilled (``value == key`` or value is empty) locale key."""


class UndefinedLocale(UserWarning):
    """Propogates when got an undefined locale."""


class UnknownModifier(UserWarning):
    """Propogates when found an unknown modifier."""
