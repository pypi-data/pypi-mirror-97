import logging
import os

import json_logging

from rasa import version

# define the version before the other imports since these need it
__version__ = version.__version__

from rasa.run import run
from rasa.train import train
from rasa.test import test

if os.environ.get('ENABLE_JSON_LOGGING', False):
    json_logging.init_non_web(enable_json=True)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(level=LOG_LEVEL)
    json_logging.config_root_logger()

logging.getLogger(__name__).addHandler(logging.NullHandler())
