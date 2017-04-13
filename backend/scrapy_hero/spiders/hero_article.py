# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy_hero.models import MysqlHandler
from scrapy_hero.items import ArticleItem

class HeroArticleSpider(scrapy.Spider):
    name = "hero_article"
    start_urls = ['http://t3.9laik.biz/pw/thread.php?fid=17/']
    start_url_pw = start_urls[0][:-1]
    topic_url_pw = 'http://t3.9laik.biz/pw/'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_hero.pipelines.SaveArticle2MySQLPipeline': 1,
        },
    }
    count = 0

    mysql_handler = MysqlHandler()
    last_offset = mysql_handler.get_offset('article')
    print 'last_offset is {0}'.format(last_offset)


    def parse(self, response):
        self.logger.info('0-----------current url is {0}'.format(response.url))
        tr_selectors = response.selector.xpath("//div[@id='main']//table[@id='ajaxtable']//tr[@class='tr3 t_one']")
        for tr_selector in tr_selectors:
            if u'置顶帖标志' != ''.join(tr_selector.xpath("td[@style='text-align:left;padding-left:8px']/img/@alt").extract()):
                topic_href = ''.join(tr_selector.xpath("td[@style='text-align:left;padding-left:8px']/h3/a/@href").extract())
                topic_title = ''.join(tr_selector.xpath("td[@style='text-align:left;padding-left:8px']/h3/a/text()").extract()).split(' ')[-1]
                self.logger.debug(topic_title)
                if topic_href:
                    if self.last_offset == topic_href:
                        self.logger.info('=====================this crawl total count is {0}================='.format(self.count))
                        return
                    else:
                        if self.count == 0:
                            self.mysql_handler.set_offset('article', topic_href)
                        yield scrapy.Request(self.topic_url_pw + topic_href, callback = self.parse_article, meta = {'title': topic_title})
                        self.count += 1

        current_page = int(response.selector.xpath("//div[@class='pages']//b/text()").extract()[0].strip())
        total_page = int(response.selector.xpath("//div[@class='pages']/a/@href").extract()[-1].split('=')[-1])
        next_page = current_page + 1
        if next_page > total_page:
            self.logger.info('=====================this crawl total count is {0}================='.format(self.count))
            return
        next_url = self.start_url_pw + '&&page={0}'.format(next_page)
        self.logger.info('current page is {0}, next page is {1}, next url is {2}'.format(current_page, next_page, next_url))
        yield scrapy.Request(next_url, callback = self.parse)

    def parse_article(self, response):
        self.logger.info('current url is {0}'.format(response.url))
        print('current url is {0}'.format(response.url))
        article_item = ArticleItem()
        #article_item['title']  = ''.join(response.selector.xpath("//h1[@id='subject_tpc']/text()").extract()).strip()
        article_item['title']  = response.meta['title']
        article_item['author']  = response.selector.xpath("//div[@class='t t2']//b/text()").extract()[0].strip()
        try:
            article_item['create_time'] = ''.join(response.selector.xpath("//div[@class='tipad']//span[@class='gray']/text()").extract()).split('Posted:')[1].strip()
        except:
            article_item['create_time'] = '{0}:00'.format(re.search(r'Posted: \d{4}-\d{2}-\d{2} \d{2}:\d{2}', response.body).group(0)[8:])

        if response.selector.xpath("//div[@id='read_tpc']/div"):
            content_str = ''.join(response.selector.xpath("//div[@id='read_tpc']/div").extract())
        else:
            content_str = ''.join(response.selector.xpath("//div[@id='read_tpc']").extract())
        
        try:
            article_item['content'] = content_str[content_str.index('>') + 1 : -6].replace('<br>', '\r\n')
        except:
            article_item['content'] = response.body[response.body.index('<div class="tpc_content" id="read_tpc">') + len('<div class="tpc_content" id="read_tpc">'): response.body.index('</div>', response.body.index('<div class="tpc_content" id="read_tpc">'))].replace('<br>', '\r\n')

        return article_item
