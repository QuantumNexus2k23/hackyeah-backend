import re
import urllib.parse

from hackyeah.routes.entities import GeocodedPlace
from hackyeah.routes.models import BasePoint


class GeocodingUrlParser:
    def __init__(self, url) -> None:
        self.url = url

    def parse(self) -> GeocodedPlace | None:
        place_re = re.search(r"place/(.+)/@(.+),(.+),(.+)/", self.url)
        if not place_re:
            return None
        lat = float(place_re.group(2))
        long = float(place_re.group(3))
        place = urllib.parse.unquote(place_re.group(1).replace("+", " "))
        return GeocodedPlace(lat, long, place)


class PointGeocodingService:
    def __init__(self, point: BasePoint, save=True):
        self.point = point
        self.save = save

    def get_geocoded_place(self) -> GeocodedPlace | None:
        return GeocodingUrlParser(self.point.google_maps_url).parse()

    def run(self) -> tuple[BasePoint, bool]:
        if not self.point.google_maps_url:
            return self.point, False

        geocoded_place = self.get_geocoded_place()
        if not geocoded_place:
            return self.point, False
        self.point.update_with_geocoded_place(geocoded_place, save=self.save)
        return self.point, True
