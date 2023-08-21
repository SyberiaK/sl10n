class DefaultLangFileNotFound(UserWarning):
    pass


class LangFileAlreadyExists(UserWarning):
    pass


class SL10nAlreadyInitialized(UserWarning):
    def __str__(self):
        return 'SL10n already initialized.'


class UndefinedLocaleKey(UserWarning):
    pass


class UnexpectedLocaleKey(UserWarning):
    pass


class UnexpectedLocale(UserWarning):
    pass
