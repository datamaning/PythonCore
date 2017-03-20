#!/usr/bin/env python
# encoding: utf-8

import scrapy

class DmozSpider(scrapy.Spider):
    name='dmoz'
    allowed_domains=['dmoz.org']
    start_urls=[
            'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
            'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
            ]
    def parse(self,response):
        filename=response.url.split('/')[-2]
        with open(filename,'wb') as f:
            item=DmozItem()
            item['title']=self.xpath('a/text()').extract()
            item['link']=self.xpath('a@href').extract()
            item['desc']=self.xpath('text()').extract()
            yield item

