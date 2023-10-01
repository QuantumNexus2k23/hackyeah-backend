from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="hackyeah API",
        default_version="v1",
        contact=openapi.Contact(email="mail@example.com"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)


api_urls = [
    path("accounts/", include("hackyeah.accounts.urls")),
    path("", include("hackyeah.routes.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/doc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", include(api_urls)),
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        kwargs={
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]
