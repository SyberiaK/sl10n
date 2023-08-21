from pathlib import Path

from sl10n import SL10n, SLocale


class Locale(SLocale):
    greetings_text: str
    pros_title: str
    pros_summary: str
    success_text: str


def demo(lang: str = 'en'):
    l10n = SL10n(Locale, Path(__file__).parent / 'lang', ignore_filenames=['tags'])

    l10n.init()  # Redumping de.json... Excluding fa.json...

    locale: Locale = l10n.locale(lang)  # Type hinted because PyCharm fails to highlight unknown attributes

    print(locale.greetings_text)
    print()
    print(locale.pros_title)
    print(locale.pros_summary)
    print()
    print(locale.success_text)
    print()
    print(f'Current locale is {locale.lang_code!r}')
    print()
    print(f'This key doesn\'t exist: {locale.get("unknown_key")}')


if __name__ == "__main__":
    demo('de')
