# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from wikiSpider.items import WikispiderItem


class MlWikiSpiderSpider(scrapy.Spider):
    # 爬虫明
    name = 'ml_wiki_spider'
    host = 'http://summonerswar.wikia.com'

    def __init__(self, *args, **kwargs):
        super(MlWikiSpiderSpider, self).__init__(*args, **kwargs)
        # 允许的域名
        self.allowed_domains = ['summonerswar.wikia.com']
        # 入口url，扔到调度器里面去
        self.start_urls = ['http://summonerswar.wikia.com/wiki/Fire_Monsters']

    '''
    解析方法，可以返回item，或者Request，或者包含二者的可迭代容器
    '''

    def parse(self, response):
        self.log(response.headers)
        ml_list = response.xpath("//div[@class='tabbertab']//table//tr[not(.//th)]")
        for i_item in ml_list:
            ml_item = WikispiderItem()
            ml_item['monster_icon'] = [
                i_item.xpath(".//td//a[@class='image image-thumbnail link-inter"
                             "nal']//img/@data-src").extract_first()]

            ml_item['monster_name'] = i_item.xpath(".//td//a[1]//text()").extract_first()

            ml_item['monster_type'] = i_item.xpath(".//td[3]//text()").extract_first().strip() \
                .replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

            ml_item['monster_max_level'] = i_item.xpath(".//td[4]//text()").extract_first().strip() \
                .replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

            ml_item['monster_hp'] = i_item.xpath(".//td[5]//text()").extract_first().strip() \
                .replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

            ml_item['monster_atk'] = i_item.xpath(".//td[6]//text()").extract_first().strip() \
                .replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

            ml_item['monster_def'] = i_item.xpath(".//td[7]//text()").extract_first().strip() \
                .replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

            ml_item['monster_spd'] = i_item.xpath(".//td[8]//text()").extract_first().strip() \
                .replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

            ml_item['monster_attribute'] = response.xpath(
                '//h1[@class="page-header__title"]/text()') \
                .extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '') \
                .replace('\r', '').strip()
            # print ml_item
            yield ml_item

        for url in response.xpath("//table[@style='width: 350px;']/tr/td/a[@class='image "
                                  "image-thumbnail link-internal']/@href").extract():
            new_url = parse.urljoin(self.host, url)
            print("new_url = " + new_url)
            # 默认打开去重
            yield scrapy.Request(url=new_url, callback=self.parse)
