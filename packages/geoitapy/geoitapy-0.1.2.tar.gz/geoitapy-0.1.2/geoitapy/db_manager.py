import os
import loggerpy
import urllib.request
import urllib.error
import zipfile
import pandas as pd

from geoitapy.exceptions import InvalidVersion
from geoitapy.util import logger_level, DATA_FIELD

logger = loggerpy.Logger()
logger.name = "geoitapy"
logger.print_level = logger_level

DATABASE_FOLDER = os.environ.get("GEOITAPY_DB_FOLDER", os.path.join(os.path.expanduser("~"), "geoitapy_database"))


def _check_version(version: str) -> bool:
    if version == "latest":
        return True
    # must start with v < v1.0 >
    if not version.startswith('v'):
        return False
    # must have a major and minor version
    cps = version[1:].split('.')
    if len(cps) != 2:
        return False
    # both must be numeric
    if not cps[0].isnumeric() or not cps[1].isnumeric():
        return False

    return True


def download_database(version: str = "latest"):
    """
    It downloads the latest version of the database if not specific version is specified.
    Otherwise the required version is searched, if not found the latest version is downloaded.

    :param version: specified version [default: latest]
    :type version: str
    :return: None
    """
    if not _check_version(version):
        raise InvalidVersion(version)

    os.makedirs(DATABASE_FOLDER, exist_ok=True)

    # if version is "latest" check which version is
    if version == "latest":
        # download last version
        urllib.request.urlretrieve("https://github.com/mett96/geoitapy/releases/download/latest/version",
                                   os.path.join(DATABASE_FOLDER, "last_version"))
        desired_version = open(os.path.join(DATABASE_FOLDER, "last_version")).read().strip()
        os.remove(os.path.join(DATABASE_FOLDER, "last_version"))
    else:
        desired_version = version

    base_url = "https://github.com/mett96/geoitapy/releases/download/{version}/geoitapy-db.zip"

    version_file = os.path.join(DATABASE_FOLDER, "version")
    # check if a version is downloaded
    if os.path.exists(version_file):
        current_version = open(version_file).read().strip()
        logger.debug(current_version, desired_version, current_version == desired_version)

        # check if the version is the same
        if current_version == desired_version:
            logger.warning("The database is in cache", source="database")
            return

    # download the desired version
    try:
        urllib.request.urlretrieve(base_url.format(version=version), os.path.join(DATABASE_FOLDER, "tmp.zip"))
    except urllib.error.HTTPError:
        logger.warning(f"Version < {version} > not found, downloaded the latest version instead", source="database")
        download_database()
        return
    # unzip the archive
    with zipfile.ZipFile(os.path.join(DATABASE_FOLDER, "tmp.zip"), 'r') as zip_file:
        zip_file.extractall(DATABASE_FOLDER)
    # remove the archive
    os.remove(os.path.join(DATABASE_FOLDER, "tmp.zip"))


def load_database() -> pd.DataFrame:
    db_path = os.path.join(DATABASE_FOLDER, 'geoitapy_db.csv')
    database = pd.read_csv(db_path,
                           sep=';',
                           encoding='utf-8',
                           dtype={"CAP": str},
                           converters={
                               "latitude": lambda x: float(x),
                               "longitude": lambda x: float(x)
                           },
                           keep_default_na=False)
    logger.debug('\n', database.dtypes)
    database.drop("link", inplace=True, axis=1)
    return database
