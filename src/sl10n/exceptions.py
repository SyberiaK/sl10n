from __future__ import annotations

import warnings


class SL10nStrictException(Exception):
    """Propogates when any warnings were raised in ``sl10n.SL10n(strict=True)``"""

    def __init__(self, warnings_list: list[warnings.WarningMessage]):
        self.exc_log = f'Caught {len(warnings_list)} warnings while parsing in strict mode:\n'
        for warning in warnings_list:
            self.exc_log += f'- {warning.category.__name__}: {warning.message}\n'

    def __str__(self):
        return self.exc_log


class SL10nIsNotInitialized(Exception):
    """Propogates when certain tasks require ``sl10n.SL10n`` to be initialized, but it wasn't."""
