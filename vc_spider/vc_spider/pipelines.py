# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from vc_spider.items import RoleSpiderItem, RoleDetailItem
from vc_spider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD, \
    TB_VCROLE_INFO


class VcSpiderPipeline(object):
    def __init__(self):
        host = MYSQL_HOST
        port = MYSQL_PORT
        db_name = MYSQL_DBNAME
        user = MYSQL_USER
        pwd = MYSQL_PASSWD

        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=pwd,
            db=db_name,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, RoleSpiderItem):
            # 名称
            name = pymysql.escape_string(item['name'])
            # 图片
            icon_url = pymysql.escape_string(item['icon_url'])
            # 属性
            attribute = pymysql.escape_string(item['attribute'])
            # 攻击距离
            attack_distance = pymysql.escape_string(item['attack_distance'])
            # 种族
            race = pymysql.escape_string(item['race'])
            # 评级
            rate = pymysql.escape_string(item['rate'])
            # 详情页url
            detail_url = pymysql.escape_string(item['detail_url'])

            sql = "insert into " + TB_VCROLE_INFO \
                  + "(name,icon_url,attribute,attack_distance" \
                    ",race,rate,detail_url)" \
                    " select %s,%s,%s,%s,%s,%s,%s" \
                    " from DUAL where not exists (select * from " + TB_VCROLE_INFO + \
                  " where icon_url = %s)"
            print(sql)
            self.cursor.execute(sql, (name, icon_url, attribute, attack_distance, race, rate,
                                      detail_url, icon_url))
            self.conn.commit()
            return item
        elif isinstance(item, RoleDetailItem):
            detail_url = pymysql.escape_string(item['detail_url'])
            arena_score = pymysql.escape_string(item['arena_score'])
            befall_score = pymysql.escape_string(item['befall_score'])
            sql = "insert into " + TB_VCROLE_INFO \
                  + "(arena_score,befall_score)" \
                    " select %s,%s" \
                    " from DUAL where not exists (select * from " + TB_VCROLE_INFO + \
                  "where detail_url = %s)"
            self.cursor.execute(sql, (arena_score, befall_score, detail_url))
            self.conn.commit()
            return item
