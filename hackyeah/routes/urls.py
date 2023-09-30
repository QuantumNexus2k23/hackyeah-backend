from rest_framework import routers

from hackyeah.routes.views import CityModelViewSet, RoutesModelViewSet

router = routers.DefaultRouter()

router.register(r"routes", RoutesModelViewSet)
router.register(r"cities", CityModelViewSet)

urlpatterns = router.urls
