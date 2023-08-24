from __future__ import annotations


class DefaultLangFileNotFound(UserWarning):
    """Propogates when the default language file not found."""
    pass


class LangFileAlreadyExists(UserWarning):
    """Propogates when the language file already exists."""
    pass


class SL10nAlreadyInitialized(UserWarning):
    """Propogates when SL10n already initialized."""

    DEFAULT_MESSAGE = 'SL10n already initialized.'

    def __init__(self, message: str | None = None):
        self.message = message if message else self.DEFAULT_MESSAGE

    def __str__(self):
        return self.message


class UndefinedLocaleKey(UserWarning):
    """Propogates when found undefined locale key."""
    pass


class UnexpectedLocaleKey(UserWarning):
    """Propogates when found unexpected locale key."""
    pass


class UndefinedLocale(UserWarning):
    """Propogates when got undefined locale."""
    pass
