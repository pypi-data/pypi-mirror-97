from .__about__ import (
    __author__,
    __commit__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __url__,
)
from .__version__ import __version__

__all__ = [
    "__author__",
    "__commit__",
    "__copyright__",
    "__email__",
    "__license__",
    "__summary__",
    "__title__",
    "__url__",
    "__version__",
]

from exorad.exorad import standard_pipeline

from exorad.cache import GlobalCache

gc = GlobalCache()
gc['n_thread'] = 1
gc['debug'] = False
