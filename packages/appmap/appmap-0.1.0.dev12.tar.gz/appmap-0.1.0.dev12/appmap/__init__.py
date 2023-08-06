"""AppMap recorder for Python"""

from ._implementation.env import Env # noqa; F401
from ._implementation.recording import Recording  # noqa: F401
from ._implementation import generation  # noqa: F401


def enabled():
    return Env.current.enabled
