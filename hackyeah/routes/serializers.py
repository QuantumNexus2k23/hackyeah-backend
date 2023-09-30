from rest_framework import serializers

from hackyeah.routes.models import RoutePoint, Route


class RoutePointSerializer(serializers.ModelSerializer):
    coordinate = serializers.SerializerMethodField()

    class Meta:
        model = RoutePoint
        fields = ("id", "name", "short_description", "coordinate")

    def get_coordinate(self, obj):
        return {"latitude": obj.latitude, "longitude": obj.longitude}


class RouteSerializer(serializers.ModelSerializer):
    route_points = RoutePointSerializer(many=True)

    class Meta:
        model = Route
        fields = ("route_points",)
