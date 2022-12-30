from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _




class SpiderAuthentication(TimeStampedModel):
    class AuthMethods(models.TextChoices):
        API_KEY = 'AK', _('API Key')
        BEARER = 'BE', _('Bearer')
        BASIC_AUTH = 'BA', _('Basic Auth')
        NO_AUTH = 'NA', _('No Auth')

    method = models.CharField(max_length=2, choices=AuthMethods.choices, default=AuthMethods.NO_AUTH)
    data = models.JSONField(default=dict)
