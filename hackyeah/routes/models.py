from pathlib import Path

from django.contrib.gis.geos import Point
from django.db import models

from hackyeah.routes.entities import GeocodedPlace

ROUTE_POINTS_IMAGE_UPLOAD_TO = Path("route_points", "images", "%Y", "%m", "%d")
ROUTE_POINTS_AUDIO_UPLOAD_TO = Path("route_points", "audio", "%Y", "%m", "%d")


class Route(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class BasePoint(models.Model):
    name = models.CharField(max_length=255, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
    short_description = models.TextField(blank=True)
    google_maps_url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"

    def update_with_geocoded_place(
        self, geocoded_place: GeocodedPlace, save=True
    ) -> None:
        self.name = self.name or geocoded_place.place
        self.longitude = geocoded_place.longitude
        self.latitude = geocoded_place.latitude
        if save:
            self.save(update_fields=["name", "longitude", "latitude"])

    @property
    def location(self) -> Point:
        return Point(self.longitude, self.latitude)


class RoutePoint(BasePoint):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    main_image = models.ImageField(
        upload_to=ROUTE_POINTS_IMAGE_UPLOAD_TO, blank=True, null=True
    )
    audio = models.FileField(
        upload_to=ROUTE_POINTS_AUDIO_UPLOAD_TO, blank=True, null=True
    )

    class Meta:
        unique_together = ("route", "order")

    def __str__(self):
        return self.name
