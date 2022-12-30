from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from .spider import Spider
from .process import SpiderProcess


class SpiderResult(TimeStampedModel):
    spider = models.ForeignKey(Spider, on_delete=models.PROTECT, db_index=True)
    parent_process = models.ForeignKey(SpiderProcess, blank=True,
                                       null=True, on_delete=models.SET_NULL,
                                       related_name='spider_result_parent_process')
    parent_result = models.ForeignKey('self', blank=True, null=True,
                                      on_delete=models.SET_NULL,
                                      related_name='spider_result_parent_result')
    child_process = models.ForeignKey(SpiderProcess, blank=True, null=True,
                                      on_delete=models.SET_NULL,
                                      related_name='spider_result_child_process')
    data = models.JSONField(default=dict)
