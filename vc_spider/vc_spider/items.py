# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 角色
class RoleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 名称
    name = scrapy.Field()
    # 图片
    icon_url = scrapy.Field()
    # 属性
    attribute = scrapy.Field()
    # 攻击距离
    attack_distance = scrapy.Field()
    # 种族
    race = scrapy.Field()
    # 评级
    rate = scrapy.Field()
    # 竞技场评分
    arena_score = scrapy.Field()
    # 降临评分
    befall_score = scrapy.Field()
    # 恢复和辅助出色的技能分析
    skill_analyze = scrapy.Field()
    # 竞技场作用分析
    arena_analyze = scrapy.Field()
    # 降临用途分析
    befall_analyze = scrapy.Field()
    # 属性耐性
    patience = scrapy.Field()
    # 主动技能
    active_skill = scrapy.Field()
    # 极限爆发
    outburst = scrapy.Field()
    # 推荐的防具、武器
    weapons = scrapy.Field()
    # 推荐的饰品
    ornament = scrapy.Field()
    # 推荐的降临
    advent_befall = scrapy.Field()

# TODO 武器item
