# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings

from wikiSpider.items import WikispiderItem


class MlWikiSpiderSpider(scrapy.Spider):
    # 爬虫明
    name = 'ml_wiki_spider'
    # 允许的域名
    allowed_domains = ['summonerswar.wikia.com']
    # 入口url，扔到调度器里面去
    start_urls = ['http://summonerswar.wikia.com/wiki/Fire_Monsters']

    def parse(self, response):
        self.log(response.headers)
        # print response.text
        ml_list = response.xpath("//div[@class='tabbertab']//table//tr[not(.//th)]")
        for i_item in ml_list:
            print(i_item)
            ml_item = WikispiderItem()
            ml_item['image_urls'] = [i_item.xpath(".//td//a[@class='image image-thumbnail link-internal']//img/@data-src").extract_first()]
            ml_item['monster_name'] = i_item.xpath(".//td//a[1]//text()").extract_first()
            ml_item['monster_type'] = i_item.xpath(".//td[3]//text()").extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            ml_item['monster_max_level'] = i_item.xpath(".//td[4]//text()").extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            ml_item['monster_hp'] = i_item.xpath(".//td[5]//text()").extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            ml_item['monster_atk'] = i_item.xpath(".//td[6]//text()").extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            ml_item['monster_def'] = i_item.xpath(".//td[7]//text()").extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            ml_item['monster_spd'] = i_item.xpath(".//td[8]//text()").extract_first().strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            # print ml_item
            yield ml_item
