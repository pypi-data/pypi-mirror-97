__version__ = "0.1.0"
__version_info__ = (0, 1, 0)

import loggerpy

logger_level = loggerpy.Level.DEBUG


def get_version():
    return __version__


DATA_FIELD = [
    "id",
    "CAP",
    "city",
    "provincia",
    "provincia_iso",
    "regione",
    "latitude",
    "longitude",
    "frazioni",
    "localita"
]
