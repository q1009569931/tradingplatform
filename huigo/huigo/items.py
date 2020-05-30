# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from product.models import mall_goods_info, mall_category


class PhoneItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = mall_goods_info

class CategoryItem(DjangoItem):
	django_model = mall_category