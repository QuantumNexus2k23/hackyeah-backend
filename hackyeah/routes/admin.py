from django.contrib import admin

from hackyeah.routes.models import Route, RoutePoint
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
    fields = ("name", "description")
    inlines = (RoutePointInline,)
