# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.http import Response

from .base import BaseSpyPipeline


class DomePipeline(BaseSpyPipeline):
    __doc__ = "This is a test Pipeline"
    __html__ = "<b>test</b>"

    def process_item(self, item, spider, last_pipeline: BaseSpyPipeline, last_response: Response):
        return item
