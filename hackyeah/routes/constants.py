from django.db import models
from django.utils.translation import gettext_lazy as _


class RouteType(models.TextChoices):
    historical = "historical", _("historical")
    artistic = "artistic", _("artistic")
