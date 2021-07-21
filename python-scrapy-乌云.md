# Scrapy wooyun实例
> 这个代码很早了，现在乌云也没了，当年我还是一名骄傲的路人甲，虽然提交的漏洞也没有厂商认领。。。
>
> gayhub有drops的备份https://wooyun.js.org/

## 1、创建项目
`scrapy startproject wooyun`
## 2、编写spider
```
cd wooyun
scrapy genspider bugs wooyun.org
cd spider
vi bugs.py
```
代码如下
```
# -*- coding: utf-8 -*-
import re
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.item import Item
from wooyun.items import WooyunItem
from scrapy.linkextractors.sgml import SgmlLinkExtractor

class BugsSpider(CrawlSpider):

    name = 'bugs'
    allowed_domains = ['wooyun.org']

    start_urls = ['http://www.wooyun.org/bugs/new_public/']

    rules = (
        Rule(SgmlLinkExtractor(allow='page/\d'), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
    #def parse(self, response):

        sel = Selector(response)

        i = WooyunItem()

        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        i['title'] = sel.xpath('//td/a/text()').extract()

        return i
```
## 2、编辑pipeline、items和settings
`vi pipelines.py`
```
# -*- coding: utf-8 -*-

class WooyunPipeline(object):
    def process_item(self, item, spider):
        for itemtmp in item['title']:
            print itemtmp
```
`vi items.py`
```
# -*- coding: utf-8 -*-
import scrapy


class WooyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    title = scrapy.Field()
```
`vi settings.py`
添加如下内容
```
ITEM_PIPELINES = {
        'wooyun.pipelines.WooyunPipeline':100
    }
```
## 3、运行实例
`scrapy crawl bugs`

# centos 6.5安装scrapy

## 1、安装python2.7
从[python download](https://www.python.org/ftp/python/)查看、选择python版本，这里以2.7的最新版本2.7.10为例 

```
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz 
tar xf Python-2.7.10.tgz 
cd Python-2.7.10 
./configure 
make all & make install 
make distclean 
rm /usr/bin/python 
ln -s /usr/local/bin/python2.7 /usr/bin/python 
```
修改默认python后yum脚本会出错，修改/usr/bin/yum第一行为 

`#!/usr/bin/python2.6`

## 2、安装pip
下载文件 
```
wget https://bootstrap.pypa.io/get-pip.py 
python get-pip.py
```

## 3、安装scrapy
`pip install scrapy `
报错，需要安装的包如下 

从[twisted download](http://twistedmatrix.com/Releases/Twisted/)查看并选择一个版本安装，这里以15.4为例 

```
wget http://twistedmatrix.com/Releases/Twisted/15.4/Twisted-15.4.0.tar.bz2 
tar xf Twisted-15.4.0.tar.bz2 
cd Twisted-15.4.0 
python setup.py install 
yum install libxml2* 
yum install libxslt* 
yum install libffi* 
```
最后再执行一次 

`pip install scrapy `

## 完成安装。 
`scrapy version`

查看结果
