from scrapy import Spider


class ProxySpider(Spider):
    name = 'ProxySpider'

    def parse(self, response):
        yield None
