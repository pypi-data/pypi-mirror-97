import os

DATABASE_FOLDER = os.environ.get("GEOITAPY_DB_FOLDER", os.path.join(os.path.expanduser("~"), "geoitapy_database"))

from .db_manager import download_database
