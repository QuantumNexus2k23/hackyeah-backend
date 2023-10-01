from rest_framework import routers

from hackyeah.routes.views import (
    CityModelViewSet,
    HeroModelViewSet,
    RoutePointModelViewSet,
    RoutesModelViewSet,
)

router = routers.DefaultRouter()

router.register(r"routes", RoutesModelViewSet)
router.register(r"cities", CityModelViewSet)
router.register(r"route-points", RoutePointModelViewSet)
router.register(r"heroes", HeroModelViewSet)

urlpatterns = router.urls
