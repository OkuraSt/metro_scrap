# -*- coding: utf-8 -*-

from pymongo import MongoClient
from metro_scrap.items.Linea import Linea
from metro_scrap.items.Estacion import Estacion

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['metro_df']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Estacion):
            self.db['Estaciones'].insert_one(dict(item))
        if isinstance(item, Linea):
            self.db['Linea'].insert_one(dict(item))
        return item
