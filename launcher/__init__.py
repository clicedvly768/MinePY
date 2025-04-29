# launcher/__init__.py
__version__ = "1.0.0"
__author__ = "Clicedvly768"

from .main import Launcher
from .database import Database

def get_version():
    return __version__