# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy_hero.items import PictureItem
from scrapy_hero.models import MysqlHandler
from scrapy.utils.project import get_project_settings

class AdultPictureSpider(scrapy.Spider):
    name = "hero_picture"
    start_urls = ['http://t3.9laik.biz/pw/thread.php?fid=15/']
    start_url_pw = start_urls[0][:-1]
    topic_url_pw = 'http://t3.9laik.biz/pw/'


    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_hero.pipelines.SaveImage2MySQLPipeline': 1,
        },
    }
    count = 0

    mysql_handler = MysqlHandler()
    last_offset = mysql_handler.get_offset('picture')


    def parse(self, response):
        self.logger.info('0-----------current url is {0}'.format(response.url))
        tr_selectors = response.selector.xpath("//div[@id='main']//table[@id='ajaxtable']//tr[@class='tr3 t_one']")
        for tr_selector in tr_selectors:
            if u'置顶帖标志' != ''.join(tr_selector.xpath("td[@style='text-align:left;padding-left:8px']/img/@alt").extract()):
                topic_href = ''.join(tr_selector.xpath("td[@style='text-align:left;padding-left:8px']/h3/a/@href").extract())
                topic_str = ''.join(tr_selector.xpath("td[@style='text-align:left;padding-left:8px']/h3/a/text()").extract())
                topic_title = re.sub(r'\[\d{2}[.-]\d{2}\]|\[\d+P\]', '', topic_str).strip()
                self.logger.debug(topic_title)
                if topic_href:
                    if self.last_offset == topic_href:
                        self.logger.info('=====================this crawl total count is {0}================='.format(self.count))
                        return
                    else:
                        if self.count == 0:
                            self.mysql_handler.set_offset('picture', topic_href)
                        yield scrapy.Request(self.topic_url_pw + topic_href, callback = self.parse_picture, meta = {'title': topic_title})
                        self.count += 1

        current_page = int(response.selector.xpath("//div[@class='pages']//b/text()").extract()[0].strip())
        total_page = int(response.selector.xpath("//div[@class='pages']/a/@href").extract()[-1].split('=')[-1])
        next_page = current_page + 1
        #if next_page > total_page:
        if next_page > 1:
            self.logger.info('=====================this crawl total count is {0}================='.format(self.count))
            return
        next_url = self.start_url_pw + '&&page={0}'.format(next_page)
        self.logger.info('current page is {0}, next page is {1}, next url is {2}'.format(current_page, next_page, next_url))
        yield scrapy.Request(next_url, callback = self.parse)

    def parse_picture(self, response):
        self.logger.info('current url is {0}'.format(response.url))
        print('current url is {0}'.format(response.url))
        picture_item = PictureItem()
        picture_item['title']  = response.meta['title']
        picture_item['author']  = response.selector.xpath("//div[@class='t t2']//b/text()").extract()[0].strip()
        try:
            picture_item['create_time'] = ''.join(response.selector.xpath("//div[@class='tipad']//span[@class='gray']/text()").extract()).split('Posted:')[1].strip()
        except:
            picture_item['create_time'] = '{0}:00'.format(re.search(r'Posted: \d{4}-\d{2}-\d{2} \d{2}:\d{2}', response.body).group(0)[8:])

        picture_url = response.selector.xpath("//div[@class='tpc_content']//img/@src").extract()
        picture_item['urls'] = [url for url in picture_url if url[:4] == 'http']

        return picture_item
