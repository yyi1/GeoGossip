import math

EARTH_RADIUS = 6371000


def calculate_bounds(lat, lon, radius):
    delta_theta = radius * 180.0 / EARTH_RADIUS / math.pi
    return lat + delta_theta, lat - delta_theta, lon + delta_theta, lon - delta_theta
    pass


def merge_categories(categories):
    if categories:
        res = list()
        for category in categories:
            res.append(category[0])
            pass
        return '\t'.join(res)
    else:
        return ''
    pass
