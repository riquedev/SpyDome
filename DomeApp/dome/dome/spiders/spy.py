import scrapy
from bootstrap import init_bootstrap

init_bootstrap()

from DomeApp.models import Spider


class SpySpider(scrapy.Spider):
    name = 'spy'

    def __init__(self, **kwargs):
        spy_id = int(kwargs['id'])
        self.spy = Spider.objects.get(pk=spy_id)
        self.start_urls = [url.url for url in self.spy.ordered_start_urls]
        super().__init__()

    def parse(self, response):
        print(response)
