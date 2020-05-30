# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from huigo.items import PhoneItem
import time

# 爬取手机信息

class IhuigoSpider(CrawlSpider):
    name = 'shouji'
    allowed_domains = ['jjhuigou.com']
    # 先调用了self.parse_start_url(response)解析下面url
    start_urls = ['http://www.jjhuigou.com/l0_1_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'jjhuigou.com/l0_\d+_\d+\.html')),
        Rule(LinkExtractor(allow=r'pid'), callback="parse_item"),
    )

    def parse_item(self, response):
        item = PhoneItem()
        item['model'] = response.xpath("//div[@class='product_intro']/div[1]/h2/text()").get().strip()
        item['brand'] = item['model'].split(' ', 1)[0]
        item['price'] = response.xpath("//div[@class='product_intro']/div[2]/ul/li[2]/div/text()").get()
        time.sleep(3)
        yield item
