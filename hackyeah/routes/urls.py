from rest_framework import routers

from hackyeah.routes.views import RoutesModelViewSet

router = routers.DefaultRouter()

router.register(r"", RoutesModelViewSet)

urlpatterns = router.urls
