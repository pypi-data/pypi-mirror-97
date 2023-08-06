import os
import sys

from .version import __version__  # noqa

sys.path.append(os.path.dirname(__file__))  # noqa

from .agilicus_api import *  # noqa
from . import patches  # noqa


ApiClient = patches.patched_api_client()
