from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", ["*"])

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# ------------- LOGGING -------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console_info": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        }
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console_info"],
        }
    },
}

# ------------- DATABASES -------------
DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}

# ------------- STATIC -------------
STATIC_ROOT = BASE_DIR.parent.joinpath("public")
MEDIA_ROOT = BASE_DIR.parent.joinpath("media")
