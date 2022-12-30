from typing import Iterator

from django.db import models
from django.db.models import QuerySet
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from .urls import SpyURL


class Spider(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=300, verbose_name=_("spider name"))
    custom_settings = models.JSONField(default=dict)
    start_urls = models.ManyToManyField(SpyURL, through='SpiderStartUrl')

    @property
    def ordered_start_urls(self) -> QuerySet[SpyURL]:
        return self.start_urls.order_by('spiderstarturl__order')


class SpiderStartUrl(models.Model):
    order = models.PositiveIntegerField()
    spider = models.ForeignKey('Spider', on_delete=models.CASCADE)
    url = models.ForeignKey(SpyURL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ('order', 'spider', 'url')
