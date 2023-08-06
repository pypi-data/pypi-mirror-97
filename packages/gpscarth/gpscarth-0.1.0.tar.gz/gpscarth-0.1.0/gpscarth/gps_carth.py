import math


class CoordinateConverter:
    def __init__(self, latitude, longitude):
        self.set_origin(latitude, longitude)
        # self.x, self.y, self.z = gps_to_carth(latitude, longitude)

    def set_origin(self, latitude, longitude):
        self.x, self.y, self.z = gps_to_carth(latitude, longitude)

    def create_gps_point(self, x, y, z):
        lat, lon = carth_to_gps(x+self.x, y+self.y, z)
        return Point(lat, lon, z)

    def create_carth_point(self, lat, lon, z):
        x, y, _ = gps_to_carth(lat, lon)
        return Point(x-self.x, y-self.y, z)


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def gps_to_carth(lat, lon, R=6378.14):
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)
    z = R * math.sin(lat)
    return x, y, z


def carth_to_gps(x, y, z, R=6378.14):
    lat = math.asin(z / R)
    lon = math.atan2(y, x)
    return lat, lon