import numpy as np
import pandas as pd

from geoitapy import database
from geoitapy.util import DATA_FIELD


def _distance_km(coo1: (tuple, list), coo2: (tuple, list)) -> float:
    from math import sin, cos, sqrt, atan2, radians

    if not isinstance(coo1, (tuple, list)) or not isinstance(coo2, (tuple, list)):
        raise TypeError("The inputted coordinates must be two tuples or lists")

    # approximate radius of earth in km
    radius = 6373.0

    lat1, lon1 = coo1
    lat2, lon2 = coo2

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return radius * c


def search_location(latitude: (float, str, tuple, list), longitude: (float, str) = None, max_distance: float = 50.0):
    __type_error = """\
A latitude and longitude must be provided as float of string. 
Otherwise pass only a tuple or list with two elements (latitude, longitude)
    """
    if longitude is None:
        if isinstance(latitude, (tuple, list)):
            latitude, longitude = latitude
        else:
            raise RuntimeError(__type_error)
    latitude = float(latitude)
    longitude = float(longitude)

    def _closest(x, lat, lon):
        return _distance_km((lat, lon), (x.latitude, x.longitude))

    database["distance"] = database.apply(_closest, axis=1, args=(latitude, longitude))
    rows = database[database.distance == database.distance.min()]
    closest_rows = rows[rows.distance < max_distance]
    
    if closest_rows.shape[0] == 0:
        print(rows)
        input('min distance too far')
        row = pd.Series([np.nan]*len(DATA_FIELD), DATA_FIELD)
    elif closest_rows.shape[0] == 1:
        row = closest_rows.iloc[0]
    else:
        group_df = closest_rows.groupby(['provincia_iso'], as_index=False)

        if len(group_df.groups) == 1:
            key = list(group_df.groups)[0]
            group = group_df.get_group(key)
        else:
            raise RuntimeError("Multiple PROV_ISO")

        row = group.apply(
            lambda x: ", ".join([str(el) for el in x.unique()]),
            axis=0
        )

    row = row.drop("id")

    return row
