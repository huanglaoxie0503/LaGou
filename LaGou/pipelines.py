# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql
from LaGou.settings import mysql_host, mysql_user, mysql_password, mysql_db
from LaGou.items import LagouItem


class LagouPipeline(object):
    """同步的方式将数据保存到数据库：方法二"""

    def __init__(self):
        self.conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            passwd=mysql_password,
            db=mysql_db,
            charset="utf8",
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            # 插入
            if isinstance(item, LagouItem):
                self.do_insert(item)
            else:
                logging.info('Error Data')
        except pymysql.Error as e:
            logging.error("-----------------insert failed-----------")
            logging.error(e)
            print(e)

        return item

    def close_spider(self, spider):
        try:
            self.conn.close()
            logging.info("mysql already close")
        except Exception as e:
            logging.info("--------mysql no close-------")
            logging.error(e)

    def do_insert(self, item):
        try:
            insert_sql, params = item.get_insert_sql()

            self.cursor.execute(insert_sql, params)
            self.conn.commit()
            logging.info("----------------insert success-----------")
        except pymysql.Error as e:
            print(e)

