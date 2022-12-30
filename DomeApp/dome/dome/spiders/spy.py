import scrapy


class SpySpider(scrapy.Spider):
    name = 'spy'
    allowed_domains = ['spy']
    start_urls = ['http://spy/']

    def parse(self, response):
        pass
