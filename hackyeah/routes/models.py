from pathlib import Path

from django.contrib.gis.geos import Point
from django.db import models

from hackyeah.routes.constants import RouteType
from hackyeah.routes.entities import GeocodedPlace

ROUTE_IMAGE_UPLOAD_TO = Path("route", "images")
ROUTE_POINTS_IMAGE_UPLOAD_TO = Path("route_points", "images")
ROUTE_POINTS_AUDIO_UPLOAD_TO = Path("route_points", "audio")
HERO_IMAGE_UPLOAD_TO = Path("route_points", "image")
PARAGRAPH_IMAGE_UPLOAD_TO = Path("route_points", "image")


class Hero(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class Route(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True, null=True, max_length=1000)
    duration = models.TimeField(default="01:00:00")
    route_type = models.CharField(
        choices=RouteType.choices, max_length=20, default=RouteType.historical
    )
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, blank=True, null=True)
    comics_url = models.URLField(blank=True, null=True, max_length=1000)

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

    class Meta:
        abstract = True

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
    route = models.ForeignKey(
        Route, related_name="route_points", on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    hero_story = models.TextField(blank=True)
    hero_quote = models.TextField(blank=True)
    main_image = models.URLField(blank=True, null=True, max_length=1000)
    audio = models.FileField(
        upload_to=ROUTE_POINTS_AUDIO_UPLOAD_TO, blank=True, null=True
    )

    class Meta:
        unique_together = ("route", "order")
        ordering = ("order",)

    def __str__(self):
        return self.name


class Paragraph(models.Model):
    order = models.PositiveSmallIntegerField()
    route_point = models.ForeignKey(
        RoutePoint, related_name="paragraphs", on_delete=models.CASCADE
    )
    text = models.TextField()
    image = models.URLField(blank=True, null=True, max_length=1000)
    image_description = models.TextField(blank=True)

    class Meta:
        unique_together = ("route_point", "order")
        ordering = ("order",)

    def __str__(self):
        return f"{self.route_point.name} - {self.order}"


class RoutePointVisit(models.Model):
    route_point = models.ForeignKey(
        RoutePoint, related_name="visited", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        related_name="visited_route_points",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("route_point", "user")
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.route_point.name} (user: {self.user_id})"
