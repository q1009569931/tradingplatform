# 介绍

**huigo-spider**是爬取[**JJ回购网**](http://www.jjhuigou.com/index.html)的爬虫，本项目已经与django项目结合，将爬取的数据通过django的orm写入MySQL数据库。本项目爬取了两个类型的信息：一是爬取网站所有手机的信息，每个手机获取它们的型号和价格，这个占大头，数据量大概有1300+条；二是爬取该网站的手机分类信息（即手机型号）。



# 启动

```powershell
python startcrawl.py
```



# 项目要点

## 集成在django项目中

在**settings.py**文件中输入

```python
import django
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'trading_platform.settings'
django.setup()
```



## 引入django的models

编辑**items.py**

```python
from scrapy_djangoitem import DjangoItem
from product.models import mall_goods_info, mall_category


class PhoneItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = mall_goods_info

class CategoryItem(DjangoItem):
	django_model = mall_category
```



## 两个爬虫文件

ihuigo.py：爬取手机信息的爬虫

```python
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
```

logo.py：爬取手机分类信息的爬虫

```python
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
```



## 爬虫多开

重写crawl命令中的run函数。在spiders同级目录下建立“mycrawls”文件夹，项目下建立两个py文件，分别是``__init__.py``和``startspiders.py``。

编辑startspiders.py

```python

import os
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError
 
 
class Command(ScrapyCommand):
 
    requires_project = True
 
    def syntax(self):
        return "[options] <spider>"
 
    def short_desc(self):
        # 这里改成 all
        return "Run all spider"
 
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
 
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')
 
    def run(self, args, opts):
        # 获取爬虫列表
        spd_loader_list = self.crawler_process.spider_loader.list()
        # 遍历各爬虫
        for spname in spd_loader_list or args:
            self.crawler_process.crawl(spname, **opts.spargs)
            print('此时启动的爬虫为：%s'%spname)
 
        self.crawler_process.start()
```

在settings.py中添加：

```python
COMMANDS_MODULE = 'huigo.mycrawls'
```



## 建立一个脚本启动爬虫

**startcrawl.py**

```python
from scrapy.cmdline import execute

# 运行所有爬虫
execute('scrapy startspiders'.split())
```



