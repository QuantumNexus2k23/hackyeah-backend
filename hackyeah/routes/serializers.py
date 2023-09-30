from rest_framework import serializers

from hackyeah.routes.models import Hero, Paragraph, Route, RoutePoint


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = "__all__"


class RoutePointSerializer(serializers.ModelSerializer):
    coordinate = serializers.SerializerMethodField()
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = RoutePoint
        fields = (
            "id",
            "name",
            "short_description",
            "coordinate",
            "main_image",
            "paragraphs",
        )

    def get_coordinate(self, obj):
        return {"latitude": obj.latitude, "longitude": obj.longitude}


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    route_points = RoutePointSerializer(many=True)
    starting_point_title = serializers.SerializerMethodField()
    hero = HeroSerializer()

    class Meta:
        model = Route
        fields = "__all__"

    @staticmethod
    def get_starting_point_title(obj: Route) -> str:
        if starting_points := obj.route_points.order_by("order").first():
            return starting_points.name
        return ""


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "name",
        )
