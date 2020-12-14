# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector


class CapterraPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(host='localhost',
                                            user='root',
                                            passwd='',
                                            database='saasrated')

        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS api_capterra""")
        self.curr.execute(
            """create table api_capterra(id integer PRIMARY KEY AUTO_INCREMENT,category text,site_id text,title text,rating text,image text,review text,feature text,price text,description text,created_date text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into api_capterra values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item['category'],
            item['site_id'],
            item['title'],
            item['rating'],
            item['image'],
            item['review'],
            item['feature'],
            item['price'],
            item['description'],
            item['created_date']

        ))
        self.conn.commit()
