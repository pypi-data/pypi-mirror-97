"""
Tools for a metamodern web environment.

## User agent tools

Simple interface, simple automate.

## Web application framework

Simple interface, simple deploy.

"""

# TODO tidy up these imports

from hstspreload import in_hsts_preload
import pendulum  # TODO XXX
from requests.exceptions import ConnectionError

from understory import mf
from understory.mkdn import render as mkdn
from understory import mm
from understory.mm import Template as template  # noqa
from understory.mm import templates  # noqa
from understory.uri import parse as uri

from . import agent
from .agent import *  # noqa
from .braid import braid, braidify
from . import framework
from .framework import *  # noqa
from .indie import *  # noqa
from .response import (Status,  # noqa
                       OK, Created, Accepted, NoContent, MultiStatus,
                       Found, SeeOther, PermanentRedirect,
                       BadRequest, Unauthorized, Forbidden, NotFound,
                       MethodNotAllowed, Conflict, Gone)
from .tasks import run_queue

__all__ = ["in_hsts_preload", "mf", "mkdn", "mm", "template", "templates",
           "pendulum", "indieauth", "micropub", "microsub", "webmention",
           "websub", "run_queue", "uri", "Created", "ConnectionError",
           "braid", "braidify"]
__all__ += agent.__all__ + framework.__all__  # noqa
