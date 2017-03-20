# -*- coding: utf-8 -*-



import scrapy
from scrapy.spiders import Spider

from scrapy.selector import Selector
import re

#from dirbot.items import Website
#from DoubanItem.items import DoubanItem
from douban.items import DoubanItem
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


class DoubanSpider(Spider):
    name = "douban"
    #allowed_domains = ["dmoz.org"]
    start_urls = ('https://www.douban.com/doulist/1264675/',)
    item=DoubanItem()
    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        selector=scrapy.Selector(response)
        books=selector.xpath('//div[@class="bd doulist-subject"]')
        for each in books:
            title = each.xpath('div[@class="title"]/a/text()').extract()[0]
            rate = each.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
            author = re.search('<div class="abstract">(.*?)<br',each.extract(),re.S).group(1)
            title = title.replace(' ','').replace('\n','')
            author = author.replace(' ','').replace('\n','')

            item['title']=title
            item['rate']=rate
            item['author']=author

            #print 'title:' + title
            #print 'rate:' + rate
            #print author
            #print ''

            yield item

