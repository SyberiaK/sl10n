from pathlib import Path

import simplejson
from sl10n import SL10n
import ujson

from . import *


def test_l10n_init_simplejson():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path, json_impl=simplejson).init()

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    locale: Locale = l10n.locale()

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == EN, f"{locale.lang_code=}, expected {EN!r}"

    assert locale.topic_title == "Basic 'for' loop algorithm", \
        f"{locale.topic_title=}, expected \"Basic 'for' loop algorithm\""
    assert locale.topic_text == TOPIC_TEXT_EN, \
        f"{locale.topic_text=}, expected '{TOPIC_TEXT_EN!r}'"
    assert locale.topic_conclusion == "Now you know basic 'for' loop algorithm!", \
        f"{locale.topic_conclusion=}, expected \"Now you know basic 'for' loop algorithm!\""


def test_l10n_init_ujson():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path, json_impl=ujson).init()

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    locale: Locale = l10n.locale()

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == EN, f"{locale.lang_code=}, expected {EN!r}"

    assert locale.topic_title == "Basic 'for' loop algorithm", \
        f"{locale.topic_title=}, expected \"Basic 'for' loop algorithm\""
    assert locale.topic_text == TOPIC_TEXT_EN, \
        f"{locale.topic_text=}, expected '{TOPIC_TEXT_EN!r}'"
    assert locale.topic_conclusion == "Now you know basic 'for' loop algorithm!", \
        f"{locale.topic_conclusion=}, expected \"Now you know basic 'for' loop algorithm!\""
