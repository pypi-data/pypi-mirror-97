import logging
from . import notebook
from .client import Session

logging.getLogger("curvenote").addHandler(logging.NullHandler())
