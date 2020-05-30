# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json

class HuigoPipeline(object):
    '''
    这里的功能，想让它可以把不同品牌的信息写入不同的文件
    '''
    # def open_spider(self, spider):
        # self.files = dict()

    def process_item(self, item, spider):
        # file = self.files.get(item["brand"])
        # if not file:
        #     path = os.getcwd()
        #     dirname = os.path.join(path, item["brand"]+"data.json")
        #     self.files[item["brand"]] = open(dirname, "w", encoding="utf-8")
        #     file = self.files[item["brand"]]
        # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # file.write(line)
        item.save()
        return item

    # def close_spider(self, spider):
        '''
        打开多个文件，就也要关闭多个文件
        '''
        # for file in self.files.values():
        #     file.close()