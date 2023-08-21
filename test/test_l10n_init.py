from pathlib import Path

import pytest

from sl10n import SL10n
from sl10n.warnings import DefaultLangFileNotFound, SL10nAlreadyInitialized, UnexpectedLocale

from . import *


def test_l10n_init():
    path = Path(__file__).parent / 'data' / 'test_l10n_init'
    l10n = SL10n(Locale, path)

    assert l10n.initialized is False, f"{l10n.initialized=}, expected False"

    with pytest.warns(DefaultLangFileNotFound):
        l10n.init()

    assert l10n.initialized is True, f"{l10n.initialized=}, expected True"


def test_l10n_init_empty():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_empty'
    with pytest.warns(DefaultLangFileNotFound):
        l10n = SL10n(Locale, path).init()

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    locale: Locale = l10n.locale()

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == EN, f"{locale.lang_code=}, expected {EN!r}"
    assert locale.topic_title == 'topic_title', f"{locale.topic_title=}, expected 'topic_title'"
    assert locale.topic_text == 'topic_text', f"{locale.topic_text=}, expected 'topic_text'"
    assert locale.topic_conclusion == 'topic_conclusion', f"{locale.topic_conclusion=}, expected 'topic_conclusion'"


def test_l10n_init_default_en():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path).init()

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    locale: Locale = l10n.locale()

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == EN, f"{locale.lang_code=}, expected {EN!r}"

    assert locale.topic_title == "Basic 'for' loop algorithm",\
        f"{locale.topic_title=}, expected \"Basic 'for' loop algorithm\""
    assert locale.topic_text == TOPIC_TEXT_EN,\
        f"{locale.topic_text=}, expected '{TOPIC_TEXT_EN!r}'"
    assert locale.topic_conclusion == "Now you know basic 'for' loop algorithm!",\
        f"{locale.topic_conclusion=}, expected \"Now you know basic 'for' loop algorithm!\""


def test_l10n_init_empty_fr():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_empty_fr'
    with pytest.warns(DefaultLangFileNotFound):
        l10n = SL10n(Locale, path, default_lang=FR).init()

    assert l10n.default_lang == FR, f"{l10n.default_lang=}, expected {FR!r}"

    locale: Locale = l10n.locale()

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == FR, f"{locale.lang_code=}, expected {FR!r}"
    assert locale.topic_title == 'topic_title', f"{locale.topic_title=}, expected 'topic_title'"
    assert locale.topic_text == 'topic_text', f"{locale.topic_text=}, expected 'topic_text'"
    assert locale.topic_conclusion == 'topic_conclusion', f"{locale.topic_conclusion=}, expected 'topic_conclusion'"


def test_l10n_init_default_fr():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_fr'
    l10n = SL10n(Locale, path, default_lang=FR).init()

    assert l10n.default_lang == FR, f"{l10n.default_lang=}, expected {FR!r}"

    locale: Locale = l10n.locale()

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == FR, f"{locale.lang_code=}, expected {FR!r}"

    assert locale.topic_title == "Algorithme de base de la boucle 'for'", \
        f"{locale.topic_title=}, expected \"Algorithme de base de la boucle 'for'\""
    assert locale.topic_text == TOPIC_TEXT_FR, \
        f"{locale.topic_text=}, expected {TOPIC_TEXT_FR!r}"
    assert locale.topic_conclusion == "Vous connaissez maintenant l'algorithme de base de la boucle 'for' !", \
        f"{locale.topic_conclusion=}, expected \"Vous connaissez maintenant l'algorithme de base de la boucle 'for' !\""


def test_l10n_init_fr_not_found():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_fr_not_found'
    l10n = SL10n(Locale, path).init()

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    with pytest.warns(UnexpectedLocale):
        locale: Locale = l10n.locale(FR)

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == EN, f"{locale.lang_code=}, expected {EN!r}"

    # Must be a copy of default lang file (EN in this example)
    assert locale.topic_title == "Basic 'for' loop algorithm", \
        f"{locale.topic_title=}, expected \"Basic 'for' loop algorithm\""
    assert locale.topic_text == TOPIC_TEXT_EN, \
        f"{locale.topic_text=}, expected '{TOPIC_TEXT_EN!r}'"
    assert locale.topic_conclusion == "Now you know basic 'for' loop algorithm!", \
        f"{locale.topic_conclusion=}, expected \"Now you know basic 'for' loop algorithm!\""


def test_l10n_warn_init_twice():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path).init()

    with pytest.warns(SL10nAlreadyInitialized):
        l10n.init()
