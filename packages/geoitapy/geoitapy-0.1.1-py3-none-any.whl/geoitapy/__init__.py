from loggerpy import Level

from geoitapy.util import __version__, __version_info__, get_version
from geoitapy.db_manager import download_database, load_database, logger

logger.print_level = Level.NO_LOGGER

download_database()
database = load_database()

from geoitapy.functions import search_location
