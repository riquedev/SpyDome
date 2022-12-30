import logging
import os
import scrapy
from bootstrap import init_bootstrap

init_bootstrap()

from django.db import connection
from DomeApp.models import Spider


class SpySpider(scrapy.Spider):
    name = 'spy'

    def get_spy(self, pk: int) -> Spider:
        self.log(Spider.objects.all())
        return Spider.objects.get(pk=pk)

    def __init__(self, **kwargs):
        spy_id = int(kwargs['id'])
        self.testing = int(kwargs.get("testing", False)) == 1

        if self.testing:
            os.environ['TEST'] = 'True' if self.testing else 'False'
            connection.creation.create_test_db(keepdb=True)

        self.spy = self.get_spy(spy_id)
        self.start_urls = [url.url for url in self.spy.ordered_start_urls]
        super().__init__()

    def parse(self, response, **kwargs):
        new_response = response
        last_pipeline = None

        for process in self.spy.ordered_processes:
            new_response = process.python_object.process_item(new_response, self, last_pipeline)
            last_pipeline = process

