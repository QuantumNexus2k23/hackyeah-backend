from dataclasses import dataclass

from django.contrib.gis.geos import Point


@dataclass
class GeocodedPlace:
    latitude: float
    longitude: float
    place: str

    @property
    def point(self):
        return Point(self.longitude, self.latitude)
