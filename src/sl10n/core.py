from __future__ import annotations

from dataclasses import fields
import json
from os import PathLike as _PathLike
from pathlib import Path
from typing import Generic, Iterable, Type, TypeVar
import sys
import warnings

if sys.version_info >= (3, 11):
    from typing import Self

from . import UTF8
from .pimpl import ParsingImpl, JSONImpl
from .process import _LocaleProcess as LocaleProcess
from .locale import SLocale
from .modifiers import PreModifiers, PostModifiers
from .warnings import DefaultLangFileNotFound, LangFileAlreadyExists, SL10nAlreadyInitialized, UndefinedLocale


T = TypeVar('T')
PathLike = TypeVar('PathLike', str, _PathLike)


class SL10n(Generic[T]):
    """
    Static text localization system.

    To use it, first create a locale container (it MUST be a subclass of `sl10n.SLocale`)
    and define some string keys in it:
    ```python
    class MyLocale(sl10n.SLocale):
        my_key_1: str
        my_key_2: str
        ...
    ```

    After that, create an SL10n object and pass in your locale container:
    ```python
    l10n = sl10n.Sl10n(MyLocale)
    ```

    Note that it only creates a reference to your localization system. To load all locale files
    and pack their content into locale containers, call `SL10n.init()` method:
    ```python
    l10n = sl10n.Sl10n(MyLocale)
    ...
    l10n.init()
    ```
    """

    default_path = Path.cwd() / 'lang'
    default_pimpl = JSONImpl(json, indent=2, ensure_ascii=False)

    def __init__(self, locale_container: Type[T], path: Path | PathLike = default_path, *, default_lang: str = 'en',
                 ignore_filenames: Iterable[str] = (), parsing_impl: ParsingImpl = default_pimpl):
        """
        Parameters:
            locale_container (Type[T]):
                Locale container to use.
                It must be an SLocale subclass.
            path (str | os.PathLike | pathlib.Path, optional):
                Path to your translation files directory. Defaults to ``pathlib.Path.cwd() / 'lang'``.
            default_lang (str, optional):
                Default language. Defaults to ``'en'``.
            ignore_filenames (Iterable[str], optional):
                What filenames the parser should ignore. Defaults to ``()``.
            parsing_impl (ParserImpl, optional):
                What JSON parsing implementation to use. Defaults to ``JSONImpl(json, indent=2, ensure_ascii=False)``.

        Raises:
            TypeError: When locale_container is not an SLocale subclass or is an SLocale itself.
        """

        self._check_locale_container(locale_container)

        self.locale_container = locale_container
        self._lc_fields = tuple(k.name for k in fields(locale_container) if k not in fields(SLocale))

        self.path = Path(path)
        self.default_lang = default_lang
        self.ignore_filenames = ignore_filenames
        self.parsing_impl = parsing_impl

        self.locales: dict[str, T] = {}
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    @staticmethod
    def _check_locale_container(locale_container) -> None:
        if not issubclass(locale_container, SLocale):
            raise TypeError('Your locale container should inherit from Locale class.')
        if locale_container == SLocale:
            raise TypeError(f'Can\'t use {SLocale.__name__} class as locale container.')

    @staticmethod
    def print_modifiers_available():
        """Print all PreModifiers and PostModifiers available."""

        print(f'PreModifiers available: {", ".join("$" + mod for mod in PreModifiers._fields)}')
        print(f'PostModifiers available: {", ".join("$" + mod for mod in PostModifiers._fields)}')

    def init(self) -> Self:
        """
        Load all locale files and pack their content into locale containers.

        You must call it to access your localization.

        Example:
            ```python
            l10n = sl10n.Sl10n(MyLocale)
            ...
            l10n.init()
            ```

            It also returns a reference to your SL10n object, so you can use this oneline to init immediately:
            ```python
            l10n = sl10n.Sl10n(MyLocale).init()
            ```
        Warns:
            SL10nAlreadyInitialized: When Sl10n is already initialized.
        """
        if self._initialized:
            warnings.warn(SL10nAlreadyInitialized(), stacklevel=2)
            return

        if not (self.path / f'{self.default_lang}.json').exists():
            warnings.warn(f'Can\'t find "{self.default_lang}.json" in locales, generating a file...',
                          DefaultLangFileNotFound, stacklevel=2)
            self.create_lang_file(self.default_lang)

        for file in self.path.glob('*.json'):
            if file.stem not in self.ignore_filenames:
                if locale := LocaleProcess(self.locale_container, file, self.parsing_impl):
                    self.locales[file.stem] = locale

        self._initialized = True
        return self

    def locale(self, lang: str | None = None) -> T:
        """
        Returns a Locale object, containing all defined string keys translated to the requested language
        (if such translation exists, otherwise returns a default one).

        Example:
            ```python
            l10n = sl10n.Sl10n(MyLocale).init()

            locale: MyLocale = l10n.locale('en')
            print(locale.my_key_1)
            ```

        Parameters:
            lang (str):
                Language you want to get.

        Raises:
            RuntimeError: When SL10n isn't initialized.

        Tip:
            We do recommend to type hint a variable where you would store a locale container.
            Some IDEs (like PyCharm) may fail to highlight unresolved attributes if you don't do so.
            ```python
            locale: MyLocale = l10n.locale('en')
            ```
        """

        if not self._initialized:
            raise RuntimeError('{0} was not initialized. Perhaps you forgot to call {0}.init()?'
                               .format(self.__class__.__name__))

        if lang is None:
            lang = self.default_lang

        if (locale := self.locales.get(lang)) is None:
            warnings.warn(f'Got unexpected lang "{lang}", returned "{self.default_lang}"',
                          UndefinedLocale, stacklevel=2)
            return self.locales[self.default_lang]

        return locale

    def create_lang_file(self, lang: str, override: bool = False):
        """
        Creates a sample lang file in a requested path.
        If you want to override existing file - set ``override`` to True.

        Useful for fast lang file creation.

        Example:
            ```python
            l10n = sl10n.Sl10n(MyLocale).init()
            l10n.create_lang_file('de')
            ```

        Parameters:
            lang (str):
                Language of translations in this file (used as filename).

            override (bool, optional):
                If ``True``, existing file will be overwritten.
                Defaults to ``False``.

        Warns:
            SL10nAlreadyInitialized: If Sl10n is initialized.
            LangFileAlreadyExists: When the file already exists and ``override`` set to ``False``

        Warning:
            Can be called **only before** SL10n initialization.
        """
        if self._initialized:
            warnings.warn(SL10nAlreadyInitialized('"create_lang_file" can be called only before Sl10n initialization.'),
                          stacklevel=2)
            return

        path = Path(self.path) / f'{lang}.json'
        if override is False and path.exists():
            warnings.warn(f'Lang file "{path}" already exists.', LangFileAlreadyExists, stacklevel=2)
            return

        p = Path(path).parent / f'{self.default_lang}.json'
        if p.exists():
            sample = LocaleProcess(self.locale_container, p, self.parsing_impl)
        else:
            sample = self.locale_container.sample()

        sample = sample.to_dict()

        keys_to_remove = set()
        for k, v in sample.items():
            if k not in self._lc_fields:
                keys_to_remove.add(k)
            if v and '\n' in v:
                sample[k] = v.split('\n')

        for k in keys_to_remove:
            del sample[k]

        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        with open(path, 'w', encoding=UTF8) as f:
            self.parsing_impl.dump(sample, f)
