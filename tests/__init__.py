from sl10n import SLocale


__all__ = ('Locale', 'EN', 'FR', 'TOPIC_TEXT_EN', 'TOPIC_TEXT_FR', 'is_equal')


class Locale(SLocale):
    topic_title: str
    topic_text: str
    topic_conclusion: str


# languages
EN = 'en'
FR = 'fr'

# topic texts on different languages
TOPIC_TEXT_EN = """1. Start loop.
2. Check the condition. If it's False - go to step 5.
3. Execute loop body.
4. Go to step 2.
5. Exit loop."""

TOPIC_TEXT_FR = """1. Démarre la boucle
2. Vérifiez la condition. Si elle est fausse, passez à l'étape 5.
3. Exécuter le corps de la boucle
4. Passer à l'étape 2.
5. Quitter la boucle."""


def is_equal(actual, expected):
    assert actual == expected, f'expected {expected!r}, got {actual!r}'
