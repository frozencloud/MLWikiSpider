# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WikispiderItem(scrapy.Item):
    # 名称
    monster_name = scrapy.Field()
    # 魔灵图片
    image_urls = scrapy.Field()
    # 魔灵类型：辅助、攻击、体力等
    monster_type = scrapy.Field()
    # 最大等级
    monster_max_level = scrapy.Field()
    # 生命值
    monster_hp = scrapy.Field()
    # 攻击力
    monster_atk = scrapy.Field()
    # 防御力
    monster_def = scrapy.Field()
    # 基础速度
    monster_spd = scrapy.Field()
    # 图片在本地的保存目录
    image_paths = scrapy.Field()