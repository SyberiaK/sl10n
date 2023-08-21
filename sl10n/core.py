from __future__ import annotations

from dataclasses import fields
import json
from os import PathLike as _PathLike
from pathlib import Path
from types import ModuleType
from typing import Generic, Iterable, Type, TypeVar
import sys
import warnings

if sys.version_info >= (3, 11):
    from typing import Self

from . import UTF8
from .process import _LocaleProcess as LocaleProcess
from .locale import SLocale
from .modifiers import PreModifiers, PostModifiers
from .warnings import DefaultLangFileNotFound, LangFileAlreadyExists, SL10nAlreadyInitialized, UnexpectedLocale


T = TypeVar('T')
PathLike = TypeVar('PathLike', str, bytes, _PathLike, Path)


class SL10n(Generic[T]):
    """
    Static text localization system.

    To use it, first create a locale container (it MUST be a subclass of `sl10n.SLocale`)
    and define some string keys in it::

      class MyLocale(sl10n.SLocale):
          my_key_1: str
          my_key_2: str
          ...

    After that, create an SL10n object and pass in your locale container::

      l10n = sl10n.Sl10n(MyLocale)

    You can also define a path where your translation files are stored, what language is default,
    what filenames should be ignored and what JSON parsing implementations to use::

      import pathlib
      import ujson  # not a stdlib

      l10n = sl10n.Sl10n(MyLocale, pathlib.Path.cwd() / 'lang',
                         default_lang='de', ignore_filenames=['tags'], json_impl=ujson)

    Note that it only creates a reference to your localization system. To load all locale files
    and pack their content into locale containers, call `SL10n.init()` method::

      l10n = sl10n.Sl10n(MyLocale)

      ...

      l10n.init()

    `SL10n.init()` returns a reference to your SL10n object, so you can use this oneline to init immediately::

      l10n = sl10n.Sl10n(MyLocale).init()

    Now you can access to your locale by using `SL10n.locale(lang)` method::

      locale = l10n.locale('en')

    It returns your locale container with specific translated strings::

      locale = l10n.locale('en')
      my_text_1 = locale.my_key_1  # 'Text 1'

    You can also access them dynamically if you need::

      locale = l10n.locale('en')
      my_text_1 = locale.get('my_key_2')  # 'Text 2'

    Strings cannot be reassigned::

      locale.my_key_2 = 'New text 2'  # Error

    All locale containers have one reserved field - `lang_code`::

      locale = l10n.locale('en')
      my_lang = locale.lang_code  # 'en'

    This field always equals to current locale lang (filename) and cannot be overwritten even from the file.
    """

    default_path = Path.cwd() / 'lang'

    def __init__(self, locale_container: Type[T], path: PathLike = None, *, default_lang: str = 'en',
                 ignore_filenames: Iterable = None, json_impl: ModuleType = json):
        self._check_locale_container(locale_container)

        self.locale_container = locale_container
        self._lc_fields = tuple(k.name for k in fields(locale_container) if k not in fields(SLocale))

        self.path = Path(path) if path else self.default_path
        self.default_lang = default_lang
        self.ignore_filenames = ignore_filenames if ignore_filenames else []
        self.json_impl = json_impl

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

        Usage::

          l10n = sl10n.Sl10n(MyLocale)

          ...

          l10n.init()

        It also returns a reference to your SL10n object, so you can use this oneline to init immediately::

          l10n = sl10n.Sl10n(MyLocale).init()
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
                if locale := LocaleProcess(self.locale_container, file, self.json_impl):
                    self.locales[file.stem] = locale

        self._initialized = True
        return self

    def locale(self, lang: str = None) -> T:
        """
        Returns a Locale object, containing all defined string keys translated to the requested language
        (if such translation exists, otherwise returns a default one).

        Usage::

          l10n = sl10n.Sl10n(MyLocale).init()

          locale: MyLocale = l10n.locale('en')
          print(locale.my_key_1)

        Parameters:
            lang (``str``):
                Language you want to get.

        Note:
            We do recommend to type hint a variable where you would store a locale container.
            Some IDEs (like PyCharm) may fail to highlight unresolved attributes if you don't do so.
            ::
             locale: MyLocale = l10n.locale('en')
        """

        if not self._initialized:
            raise RuntimeError('{0} was not initialized. Perhaps you forgot to call {0}.init()?'
                               .format(self.__class__.__name__))

        if lang is None:
            lang = self.default_lang

        if (locale := self.locales.get(lang)) is None:
            warnings.warn(f'Got unexpected lang "{lang}", returned "{self.default_lang}"',
                          UnexpectedLocale, stacklevel=2)
            return self.locales[self.default_lang]

        return locale

    def create_lang_file(self, lang: str, override: bool = False):
        """
        Creates a sample lang file in a requested path.
        If you want to override existing file - set ``override`` to True.

        Useful for fast lang file creation.

        Usage::

          l10n = sl10n.Sl10n(MyLocale).init()
          l10n.create_lang_file('de')

        Parameters:
            lang (``str``):
                Language of translations in this file (used as filename).

            override (``bool``, *optional*):
                If ``True``, existing file will be overwritten.
                Defaults to ``False``.

        Note:
            Can be called ONLY BEFORE SL10n initialization.
            Issues a LangFileAlreadyExists warning if file already exists and ``override`` set to ``False``.
        """
        if self._initialized:
            warnings.warn('"create_lang_file" can be called only before Sl10n initialization.',
                          SL10nAlreadyInitialized, stacklevel=2)
            return

        path = Path(self.path) / f'{lang}.json'
        if override is False and path.exists():
            warnings.warn(f'Lang file "{path}" already exists.', LangFileAlreadyExists, stacklevel=2)
            return

        p = Path(path).parent / f'{self.default_lang}.json'
        if p.exists():
            sample = LocaleProcess(self.locale_container, p, self.json_impl)
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
            self.json_impl.dump(sample, f, indent=2, ensure_ascii=False)
