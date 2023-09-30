from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from hackyeah.routes.models import City, Route, RoutePoint, RoutePointVisit
from hackyeah.routes.serializers import (
    CitySerializer,
    RoutePointSerializer,
    RoutePointVisitSerializer,
    RouteSerializer,
)


class RoutesModelViewSet(ReadOnlyModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    filterset_fields = ("city_id",)

    def get_permissions(self):
        if self.action in ["visit", "clean_progress"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    @swagger_auto_schema(
        request_body=RoutePointVisitSerializer,
        responses={status.HTTP_201_CREATED: "ok"},
    )
    def visit(self, request, pk: int):
        self.get_object()
        serializer = RoutePointVisitSerializer(
            data=request.data, context={"request": request, "route_id": pk}
        )
        serializer.is_valid(raise_exception=True)
        RoutePointVisit.objects.get_or_create(
            route_point_id=serializer.data["point"], user=request.user
        )
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=no_body, responses={status.HTTP_204_NO_CONTENT: "deleted"}
    )
    @action(detail=True, methods=["post"], url_path="clean-progress")
    def clean_progress(self, request, pk: int):
        """
        Delete all user's progress for a given route
        """
        self.get_object()
        RoutePointVisit.objects.filter(
            user=self.request.user, route_point_id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoutePointModelViewSet(ReadOnlyModelViewSet):
    serializer_class = RoutePointSerializer
    queryset = RoutePoint.objects.all()


class CityModelViewSet(ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
