# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from cassandra.cqlengine import connection
#from cassandra.cqlengine import management

import os
import scrapy

from models import MysqlHandler, Article, Picture

from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

class ScrapyAudltPipeline(object):
    def process_item(self, item, spider):
        return item

#class SaveArticle2MongoPipeline(object):
#    def __init__(self):
#        settings = get_project_settings()
#        self.mongo_handler = MongoHandler(
#            settings.get('MONGO_HOST'),
#            settings.get('MONGO_PORT'),
#            settings.get('MONGO_USER'),
#            settings.get('MONGO_PASS'),
#            settings.get('MONGO_DB_HERO')
#        )
#        return
#
#    def process_item(self, item, spider):
#        article_model = Article(
#            title = item['title'],
#            author = item['author'],
#            create_time = item['create_time'],
#            content = item['content']
#        )
#        article_model.save()
#        return item

class SaveArticle2MySQLPipeline(object):
    def __init__(self):
        self.session = None
        self.mysql_handler = MysqlHandler()
        return
    def process_item(self, item, spider):
        article_model = Article(
            title = item['title'],
            author = item['author'],
            create_time = item['create_time'],
            content = item['content']
        )
        
        self.session = self.mysql_handler.get_session()
        self.session.add(article_model)
        self.session.commit()
        self.session.close()
        return item

#class SaveImage2MongoPipeline(ImagesPipeline):
#
#    def get_media_requests(self, item, info):
#        for image_url in item['urls']:
#            print image_url
#            yield scrapy.Request(image_url)
#
#    
#    def item_completed(self, results, item, info):
#        image_paths = [x['path'] for ok, x in results if ok]
#        if not image_paths:
#            raise DropItem("Item contains no images")
#
#        settings = get_project_settings()
#        original_save_path = settings.get('IMAGES_STORE') + '/' + os.path.dirname(image_paths[0])
#        new_save_path = settings.get('IMAGES_STORE') + '/' + item['create_time'].split()[0] + '/' + item['title']
#        if not os.path.exists(new_save_path):
#            os.makedirs(new_save_path)
#        save_paths = []
#        for original_path in image_paths:
#            original_path_file = os.path.join(original_save_path, os.path.basename(original_path))
#            new_path_file = os.path.join(new_save_path, os.path.basename(original_path_file))
#            os.rename(original_path_file, new_path_file)
#            save_paths.append(new_path_file)
#        item['paths'] = save_paths
#        return item

class SaveImage2MySQLPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        settings = get_project_settings()
        original_save_path = settings.get('IMAGES_STORE') + '/' + os.path.dirname(image_paths[0])
        new_save_path = settings.get('IMAGES_STORE') + '/' + item['create_time'].split()[0] + '/' + item['title']
        if not os.path.exists(new_save_path):
            os.makedirs(new_save_path)
        save_paths = []
        for original_path in image_paths:
            original_path_file = os.path.join(original_save_path, os.path.basename(original_path))
            new_path_file = os.path.join(new_save_path, os.path.basename(original_path_file))
            os.rename(original_path_file, new_path_file)
            save_paths.append(new_path_file)
        item['paths'] = save_paths

        picture_model = Picture(
            title = item['title'],
            author = item['author'],
            create_time = item['create_time'],
            paths = ','.join(item['paths'])
        )
        mysql_handler = MysqlHandler()
        session = mysql_handler.get_session()
        session.add(picture_model)
        session.commit()
        session.close()
        return item
