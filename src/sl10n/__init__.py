"""Static localization system that reduces the headache of working with localization"""

__version__ = '0.2.0'

import logging

UTF8 = 'utf-8'
LOGGER = logging.getLogger('sl10n')

LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | sl10n: %(message)s', '%H:%M:%S — %d/%m/%Y')
stream_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)

from .core import SL10n
from .locale import SLocale
