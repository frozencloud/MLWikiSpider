# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from wikiSpider.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PORT, TB_BASE_INFO


class WikispiderPipeline(object):
    def __init__(self):
        host = MYSQL_HOST
        port = MYSQL_PORT
        dbname = MYSQL_DBNAME
        user = MYSQL_USER
        pwd = MYSQL_PASSWD

        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=pwd,
            db=dbname,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        name = pymysql.escape_string(item['monster_name'])
        icon = pymysql.escape_string(item['monster_icon'])
        type = pymysql.escape_string(item['monster_type'])
        maxlevel = pymysql.escape_string(item['monster_max_level'])
        hp = pymysql.escape_string(item['monster_hp'])
        atk = pymysql.escape_string(item['monster_atk'])
        deff = pymysql.escape_string(item['monster_def'])
        spd = pymysql.escape_string(item['monster_spd'])

        sql = "insert into " + TB_BASE_INFO + "(monster_name,monster_icon,monster_type,monster_max_level,monster_hp" \
                                              ",monster_atk,monster_def,monster_spd) select %s,%s,%s,%s,%s,%s,%s,%s" \
                                              " from DUAL where not exists (select * from tb_base_info " \
                                              "where monster_icon = %s)"
        self.cursor.execute(sql, (name, icon, type, maxlevel, hp, atk, deff, spd,icon))
        self.conn.commit()
        return item
