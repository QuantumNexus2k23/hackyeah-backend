import dj_database_url

from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False
SECRET_KEY = "secret_key"

# ------------- DATABASES -------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", "hackyeah"),
        "USER": env("POSTGRES_USER", "hackyeah"),
        "PASSWORD": env("POSTGRES_PASSWORD", "hackyeah"),
        "HOST": env("POSTGRES_HOST", "localhost"),
        "PORT": env("POSTGRES_PORT", "5432"),
    }
}

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "rest_framework.authentication.SessionAuthentication",
)
# DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
print(DATABASES)
