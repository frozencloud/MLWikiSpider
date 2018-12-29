# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import shutil

import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

from wikiSpider.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PORT, \
    TB_BASE_INFO


class WikispiderPipeline(object):
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
        name = pymysql.escape_string(item['monster_name'])
        icon = pymysql.escape_string(item['monster_icon'][0])
        monster_type = pymysql.escape_string(item['monster_type'])
        max_level = pymysql.escape_string(item['monster_max_level'])
        hp = pymysql.escape_string(item['monster_hp'])
        atk = pymysql.escape_string(item['monster_atk'])
        deff = pymysql.escape_string(item['monster_def'])
        spd = pymysql.escape_string(item['monster_spd'])
        monster_attribute = pymysql.escape_string(item['monster_attribute'])

        sql = "insert into " + TB_BASE_INFO \
              + "(monster_name,monster_icon,monster_type,monster_max_level,monster_hp" \
                ",monster_atk,monster_def,monster_spd,monster_attribute)" \
                " select %s,%s,%s,%s,%s,%s,%s,%s,%s" \
                " from DUAL where not exists (select * from tb_base_info " \
                "where monster_icon = %s)"
        self.cursor.execute(sql, (name, icon, monster_type, max_level, hp, atk, deff, spd
                                  , monster_attribute, icon))
        self.conn.commit()
        return item


class WikiImagePipelines(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')
    host = MYSQL_HOST
    port = MYSQL_PORT
    db_name = MYSQL_DBNAME
    user = MYSQL_USER
    pwd = MYSQL_PASSWD

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        passwd=pwd,
        db=db_name,
        charset='utf8',
        use_unicode=True)
    cursor = conn.cursor()

    '''
    返回值：
    [
        (True,
          {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
           'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
           'url': 'http://www.example.com/files/product1.pdf'}),
        (False,
            Failure(...))]
            给到item_completed
    '''

    def get_media_requests(self, item, info):
        for image_url in item['monster_icon']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        # 将下载的图片路径（传入到results中）存储到 image_paths 项目组中，如果其中没有图片，我们将丢弃项目:
        image_path = [x['path'] for ok, x in results if ok][0]
        image_url = [y['url'] for ok, y in results if ok][0]
        if not image_path:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_path

        # 定义分类保存的路径
        # print(image_path)
        #
        # for v in image_path, image_url:

        # 更新数据库
        sql_str = 'update ' + TB_BASE_INFO + ' set icon_local_path = %s where monster_icon = %s'
        self.cursor.execute(sql_str, (image_path, image_url))
        self.conn.commit()

            # pic_name = v.replace('full/', '')
            # pic_big_name = pic_name.replace('.jpg', '') + '_b.jpg'
            # shutil.move(self.img_store + '\\full\\' + pic_name, pic_name)
            # shutil.move(self.img_store + '\\thumbs\\big\\' + pic_name, pic_big_name)

        return item
