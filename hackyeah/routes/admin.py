from django.contrib import admin

from hackyeah.routes.models import (
    City,
    Hero,
    Paragraph,
    Route,
    RoutePoint,
    RoutePointVisit,
)
from hackyeah.routes.services import PointGeocodingService


@admin.register(RoutePoint)
class RoutePointAdmin(admin.ModelAdmin):
    list_display = ("name", "display_location", "route")

    @admin.display(description="Location")
    def display_location(self, obj):
        return f"{obj.latitude}, {obj.longitude}"

    def save_model(self, request, obj, form, change):
        if obj.google_maps_url:
            obj, updated = PointGeocodingService(obj, save=False).run()
        return super().save_model(request, obj, form, change)


class RoutePointInline(admin.TabularInline):
    model = RoutePoint
    fields = ("order", "name", "short_description", "longitude", "latitude")
    readonly_fields = ("longitude", "latitude")
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = (RoutePointInline,)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "display_route",
        "route_point",
    )
    list_filter = ("route_point__route",)

    @admin.display(description="Route")
    def display_route(self, obj):
        return obj.route_point.route


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass


@admin.register(RoutePointVisit)
class RoutePointVisitAdmin(admin.ModelAdmin):
    pass
