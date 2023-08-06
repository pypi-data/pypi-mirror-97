"""
Short for Seeq PYthon, the SPy library provides methods to interact with data that is exposed to the Seeq Server.
"""

from . import assets
from . import docs
from . import workbooks
from . import widgets
from . import utils

from ._login import login, logout
from ._plot import plot
from ._pull import pull
from ._push import push
from ._search import search
from ._common import PATH_ROOT, DEFAULT_WORKBOOK_PATH, Status
from ._config import options

client = None
user = None
server_version = None

__all__ = ['assets', 'docs', 'workbooks', 'widgets', 'login', 'logout', 'plot', 'pull', 'push', 'search',
           'PATH_ROOT', 'DEFAULT_WORKBOOK_PATH', 'Status', 'options', 'client', 'user', 'server_version']
