from rest_framework import serializers

from hackyeah.routes.models import RoutePoint, Route


class RoutePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePoint


class RouteSerializer(serializers.ModelSerializer):
    routepoint_set = RoutePointSerializer(many=True)

    class Meta:
        model = Route
        fields = ("name", "description", "routepoint_set")
