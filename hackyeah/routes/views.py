from rest_framework.viewsets import ReadOnlyModelViewSet

from hackyeah.routes.models import Route
from hackyeah.routes.serializers import RouteSerializer


class RoutesModelViewSet(ReadOnlyModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
