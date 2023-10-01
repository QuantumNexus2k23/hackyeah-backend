from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from hackyeah.routes.models import Hero, Paragraph, Route, RoutePoint, RoutePointVisit


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = "__all__"


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class RoutePointSerializer(serializers.ModelSerializer):
    coordinate = serializers.SerializerMethodField()
    paragraphs = ParagraphSerializer(many=True)
    visited_by_user = serializers.SerializerMethodField()

    class Meta:
        model = RoutePoint
        fields = (
            "id",
            "name",
            "short_description",
            "description",
            "coordinate",
            "main_image",
            "visited_by_user",
            "paragraphs",
        )

    @swagger_serializer_method(serializer_or_field=CoordinatesSerializer)
    def get_coordinate(self, obj):
        return {"latitude": obj.latitude, "longitude": obj.longitude}

    def get_visited_by_user(self, obj: RoutePoint) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return RoutePointVisit.objects.filter(
                user=request.user, route_point=obj
            ).exists()
        return False


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    route_points = RoutePointSerializer(many=True)
    starting_point_title = serializers.SerializerMethodField()
    hero = HeroSerializer()
    visited_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = "__all__"

    @staticmethod
    def get_starting_point_title(obj: Route) -> str:
        if starting_points := obj.route_points.order_by("order").first():
            return starting_points.name
        return ""

    def get_visited_by_user(self, obj: Route) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return (
                RoutePointVisit.objects.filter(
                    user=request.user, route_point__route=obj
                ).count()
                == obj.route_points.count()
            )
        return False


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "name",
        )


class RoutePointVisitSerializer(serializers.ModelSerializer):
    point = serializers.PrimaryKeyRelatedField(
        queryset=RoutePoint.objects.all(), source="id"
    )

    class Meta:
        model = RoutePoint
        fields = ("point",)

    def validate(self, attrs):
        if str(attrs["id"].route_id) != str(self.context["route_id"]):
            raise serializers.ValidationError(
                "Route point does not belong to the route"
            )
        return attrs
