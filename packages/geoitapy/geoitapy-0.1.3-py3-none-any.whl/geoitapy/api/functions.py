def distance_km(coo1: (tuple, list), coo2: (tuple, list)) -> float:
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
