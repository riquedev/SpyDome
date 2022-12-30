from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from .urls import SpyURL


class SpiderStartUrl(models.Model):
    order = models.PositiveIntegerField()
    spider = models.ForeignKey('Spider', on_delete=models.CASCADE)
    url = models.ForeignKey(SpyURL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']


class Spider(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=300, verbose_name=_("spider name"))
    custom_settings = models.JSONField(default=dict)
    start_urls = models.ManyToManyField(SpyURL, through='SpiderStartUrl')
