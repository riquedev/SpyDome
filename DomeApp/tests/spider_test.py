from django.test import TestCase
from DomeApp.models import (Spider, SpiderStartUrl, SpyURL)


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
