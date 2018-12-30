from urllib import parse

from scrapy import Spider, Request

from vc_spider.items import RoleSpiderItem


class VcSpider(Spider):
    name = 'vc_spider'
    host = 'https://altema.jp/valkyrieconnect'

    def __init__(self, *args, **kwargs):
        super(VcSpider, self).__init__(*args, **kwargs)
        # 允许的域名
        self.allowed_domains = ['altema.jp']
        # 入口url，扔到调度器里面去
        self.start_urls = ['https://altema.jp/valkyrieconnect/charaichiran']

    def parse(self, response):
        role_list = response.xpath('//table[@class="all-center"]//tr[not(.//th)]')
        for item in role_list:
            role_item = RoleSpiderItem()
            role_item['name'] = item.xpath('')
            role_item['icon_url'] = item.xpath('')
            role_item['attribute'] = item.xpath('')
            role_item['attack_distance'] = item.xpath('')
            role_item['race'] = item.xpath('')
            role_item['rate'] = item.xpath('')
        yield role_item

        for i in role_list:
            new_url = i.xpath('')
            new_url = parse.urljoin(self.host, new_url)
            print("new_url = " + new_url)
        yield Request(url=new_url, callback=self.parse2)

    def parse2(self, response):

        pass
