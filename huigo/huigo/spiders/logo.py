# -*- coding: utf-8 -*-
import scrapy
from huigo.items import CategoryItem
import time

# 爬取分类信息
class LogoSpider(scrapy.Spider):
	name = 'logo'
	allowed_domains = ['jjhuigou.com']
	start_urls = ['http://www.jjhuigou.com/l0_1_1.html']

	def parse(self, response):
		
		logo = response.xpath("//*[@id='pinpai_li_1']/a/label/text()")
		for i in logo:
			item = CategoryItem()
			item["name"] = i.get()
			time.sleep(1)
			yield item
