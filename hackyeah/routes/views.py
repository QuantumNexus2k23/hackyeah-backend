from rest_framework.viewsets import ReadOnlyModelViewSet

from hackyeah.routes.models import City, Route
from hackyeah.routes.serializers import CitySerializer, RouteSerializer


class RoutesModelViewSet(ReadOnlyModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    filterset_fields = ("city_id",)


class CityModelViewSet(ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
