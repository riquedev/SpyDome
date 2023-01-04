from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from mirage import fields


class SpiderAuthentication(TimeStampedModel):
    """
    Model responsible for storing data that will be used in the authentication process.
    We use django-mirage-fields to ensure credential security.
    """

    class AuthMethods(models.TextChoices):
        API_KEY = 'AK', _('API Key')
        BEARER = 'BE', _('Bearer')
        BASIC_AUTH = 'BA', _('Basic Auth')
        NO_AUTH = 'NA', _('No Auth')

    method = models.CharField(max_length=2, choices=AuthMethods.choices, default=AuthMethods.NO_AUTH)
    data = fields.EncryptedJSONField(default=dict)
