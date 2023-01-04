from django.db import models
from django_extensions.db.models import TimeStampedModel
from mirage import fields
from .spider import Spider
from .process import SpiderProcess
import json
class SpiderResult(TimeStampedModel):
    """
    This model is responsible for storing data referring
    to the steps taken by the Spider, in this step we perform
    the security of the collected data.
    """
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
    data = fields.EncryptedJSONField(default=dict)

    @classmethod
    def jsonfy(cls, value) -> str:
        data = {'value': value, "error": None}
        try:
            data['value'] = value
        except json.JSONDecodeError as er:
            data["error"] = str(er)

        return json.dumps(data)
