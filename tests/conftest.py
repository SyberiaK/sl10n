import builtins
import io
import os

import pytest


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
