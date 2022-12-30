from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel


class SpyURL(TimeStampedModel, ActivatorModel):
    url = models.URLField()
