from pathlib import Path

import pytest

from sl10n import SL10n
from sl10n.warnings import DefaultLangFileNotFound, SL10nAlreadyInitialized, UndefinedLocale

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

    is_equal(l10n.default_lang, EN)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.topic_title, 'topic_title')
    is_equal(locale.topic_text, 'topic_text')
    is_equal(locale.topic_conclusion, 'topic_conclusion')


def test_l10n_init_default_en():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path).init()

    is_equal(l10n.default_lang, EN)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")


def test_l10n_init_empty_fr():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_empty_fr'
    with pytest.warns(DefaultLangFileNotFound):
        l10n = SL10n(Locale, path, default_lang=FR).init()

    is_equal(l10n.default_lang, FR)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, FR)
    is_equal(locale.topic_title, 'topic_title')
    is_equal(locale.topic_text, 'topic_text')
    is_equal(locale.topic_conclusion, 'topic_conclusion')


def test_l10n_init_default_fr():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_fr'
    l10n = SL10n(Locale, path, default_lang=FR).init()

    is_equal(l10n.default_lang, FR)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, FR)
    is_equal(locale.topic_title, "Algorithme de base de la boucle 'for'")
    is_equal(locale.topic_text, TOPIC_TEXT_FR)
    is_equal(locale.topic_conclusion, "Vous connaissez maintenant l'algorithme de base de la boucle 'for' !")


def test_l10n_init_fr_not_found():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_fr_not_found'
    l10n = SL10n(Locale, path).init()

    is_equal(l10n.default_lang, EN)

    with pytest.warns(UndefinedLocale):
        locale: Locale = l10n.locale(FR)
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)

    # Must be a default locale (EN in this example)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")


def test_l10n_warn_init_twice():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path).init()

    with pytest.warns(SL10nAlreadyInitialized):
        l10n.init()
