from urllib import parse

from scrapy import Spider, Request

from vc_spider.items import RoleSpiderItem, RoleDetailItem


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
        # print(response.text)
        role_list = response.xpath('//table[@class="all-center"]//tr[contains(@class,"data-row")]')
        for item in role_list:
            print(item)
            role_item = RoleSpiderItem()
            role_item['name'] = item.xpath('.//a//img/@title').extract_first()
            role_item['icon_url'] = item.xpath('.//a//img//@data-lazy-src').extract_first()
            role_item['attribute'] = item.xpath('.//td[2]//text()').extract_first()
            role_item['attack_distance'] = item.xpath('.//td[3]//text()').extract_first()
            role_item['race'] = item.xpath('.//td[4]//text()').extract_first()
            role_item['rate'] = item.xpath('.//span[contains(@style,"text-align:center") and '
                                           'contains(@style,"display:block")]//text()').\
                extract_first()
            a = item.xpath('.//td[@style="text-align: center;"]//a//@href').extract_first()
            role_item['detail_url'] = parse.urljoin(self.host, a)
            yield role_item

        for i in role_list:
            new_url = i.xpath('.//td[@style="text-align: center;"]//a//@href').extract_first()
            new_url = parse.urljoin(self.host, new_url)
            print("new_url = " + new_url)
            yield Request(url=new_url, callback=self.parse2)

    def parse2(self, response):
        detail_list = response.xpath('//div[@class="contents clearfix"]')
        # print(response.text)
        for item in detail_list:
            detail_item = RoleDetailItem()

            detail_item['detail_url'] = response.url
            # 评级
            detail_item['rate'] = item.xpath('.//table[@class="tableLine"]//tr//td[1]//span[contains(@style,"font-weight: bold") and contains(@style,"font-size: 200%")]//text()').extract_first()
            # 竞技场评分
            detail_item['arena_score'] = item.xpath('.//table[@class="tableLine"]//tr//td[2]//span[@class="tensu redtxt"]//text()').extract_first()
            # 降临评分
            detail_item['befall_score'] = item.xpath(
                './/table[@class="tableLine"]//tr//td[3]//span[@class="tensu redtxt"]//text()').extract_first()
            # # 技能分析
            # detail_item['skill_analyze'] = item.xpath('')
            # # 竞技场作用分析
            # detail_item['arena_analyze'] = item.xpath('')
            # # 降临用途分析
            # detail_item['befall_analyze'] = item.xpath('')
            # # 属性耐性
            # detail_item['patience'] = item.xpath('')
            # # 主动技能
            # detail_item['active_skill'] = item.xpath('')
            # # 极限爆发
            # detail_item['outburst'] = item.xpath('')
            # # 推荐的防具、武器
            # detail_item['weapons'] = item.xpath('')
            # # 推荐的饰品
            # detail_item['ornament'] = item.xpath('')
            # # 推荐的降临
            # detail_item['advent_befall'] = item.xpath('')
            yield detail_item
