from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from .spider import Spider


class SpiderProcess(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=300, verbose_name=_("spider process name"))
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'spider')