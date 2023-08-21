import builtins
import io
import os

import pytest
from sl10n import SLocale


__all__ = ('Locale', 'EN', 'FR', 'TOPIC_TEXT_EN', 'TOPIC_TEXT_FR', 'cleanup_files')


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


def patch_open(open_func, files):
    def open_patched(path, mode='r', buffering=-1, encoding=None,
                     errors=None, newline=None, closefd=True,
                     opener=None):
        if 'w' in mode and not os.path.isfile(path):
            files.append(path)
        return open_func(path, mode=mode, buffering=buffering,
                         encoding=encoding, errors=errors,
                         newline=newline, closefd=closefd,
                         opener=opener)
    return open_patched


@pytest.fixture(autouse=True)
def cleanup_files(monkeypatch):
    files = []
    monkeypatch.setattr(builtins, 'open', patch_open(builtins.open, files))
    monkeypatch.setattr(io, 'open', patch_open(io.open, files))
    yield
    for file in files:
        os.remove(file)
