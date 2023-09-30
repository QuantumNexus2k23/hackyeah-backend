from rest_framework import routers

from hackyeah.routes.views import (
    CityModelViewSet,
    RoutePointModelViewSet,
    RoutesModelViewSet,
)

router = routers.DefaultRouter()

router.register(r"routes", RoutesModelViewSet)
router.register(r"cities", CityModelViewSet)
router.register(r"route-points", RoutePointModelViewSet)

urlpatterns = router.urls
