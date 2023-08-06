__version__ = '1.3.1'

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from ._charts import *  # noqa: F403
    from .models import AnnotationModel  # noqa: F401
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
