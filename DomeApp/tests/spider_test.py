from django.test import TestCase
from DomeApp.models import (Spider, SpiderStartUrl, SpyURL)
from DomeApp.models.spider import on_spy_finished, SpiderCall
from scrapy.crawler import CrawlerProcess
from DomeApp.dome.dome.spiders.spy import SpySpider

class SpiderTest(TestCase):
    def setUp(self):
        self.spider = Spider.objects.create(name="Test Spider")
        self.url1 = SpyURL.objects.create(url="https://github.com/")
        self.url2 = SpyURL.objects.create(url="https://stackoverflow.com/")
        SpiderStartUrl.objects.create(
            spider=self.spider,
            url=self.url1,
            order=2
        )
        SpiderStartUrl.objects.create(spider=self.spider,
                                      url=self.url2,
                                      order=1)

    def test_start_url_order(self):
        qs_start_urls = SpiderStartUrl.objects.all().values_list(
            'url__url', flat=True
        )
        qs_spider = self.spider.ordered_start_urls.values_list(
            'url', flat=True
        )
        qs_spider_urls = self.spider.start_urls.all().values_list('url', flat=True)
        self.assertEqual(list(qs_start_urls), list(qs_spider))
        self.assertNotEqual(list(qs_start_urls), list(qs_spider_urls))
        self.assertNotEqual(list(qs_spider), list(qs_spider_urls))

    def test_call_spy(self):
        thread = self.spider.initialize(is_test=True)
        # i don't know how use a test connection in thread
        # thread.join()
        c = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0', 'LOG_FILE': 'test_call_spy.log'})
        c.crawl(SpySpider, id=self.spider.pk)
        c.start()
        kwargs = {
            'output': open('test_call_spy.log', 'r').read(),
            'error': '',
            'call': thread
        }
        on_spy_finished(self.spider, **kwargs)


