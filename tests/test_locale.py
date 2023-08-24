from pathlib import Path

import pytest

from sl10n import SL10n
from sl10n.warnings import DefaultLangFileNotFound, UndefinedLocale, UnexpectedLocaleKey

from . import *


@pytest.mark.parametrize("lang_code", [EN, FR])
def test_locale_empty(lang_code):
    path = Path(__file__).parent / 'data' / 'test_locale_empty'
    with pytest.warns(DefaultLangFileNotFound):
        l10n = SL10n(Locale, path, default_lang=lang_code).init()

    is_equal(l10n.default_lang, lang_code)

    locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, lang_code)
    is_equal(locale.topic_title, 'topic_title')
    is_equal(locale.topic_text, 'topic_text')
    is_equal(locale.topic_conclusion, 'topic_conclusion')


@pytest.mark.parametrize("lang_code,topic_title,topic_text,topic_conclusion", [
    (EN, "Basic 'for' loop algorithm",
     TOPIC_TEXT_EN, "Now you know basic 'for' loop algorithm!"),
    (FR, "Algorithme de base de la boucle 'for'",
     TOPIC_TEXT_FR, "Vous connaissez maintenant l'algorithme de base de la boucle 'for' !")
])
def test_locale_default(lang_code, topic_title, topic_text, topic_conclusion):
    path = Path(__file__).parent / 'data' / f'test_locale_{lang_code}'
    l10n = SL10n(Locale, path, default_lang=lang_code).init()

    is_equal(l10n.default_lang, lang_code)

    locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, lang_code)
    is_equal(locale.topic_title, topic_title)
    is_equal(locale.topic_text, topic_text)
    is_equal(locale.topic_conclusion, topic_conclusion)


def test_locale_fr_not_found():
    path = Path(__file__).parent / 'data' / 'test_locale_en'
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


def test_locale_dynamic_access():
    path = Path(__file__).parent / 'data' / 'test_locale_en'
    l10n = SL10n(Locale, path).init()

    is_equal(l10n.default_lang, EN)

    locale = l10n.locale()

    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.get('topic_title'), "Basic 'for' loop algorithm")
    is_equal(locale.get('topic_text'), TOPIC_TEXT_EN)
    is_equal(locale.get('topic_conclusion'), "Now you know basic 'for' loop algorithm!")
    with pytest.warns(UnexpectedLocaleKey):
        is_equal(locale.get('unknown_key'), 'unknown_key')
