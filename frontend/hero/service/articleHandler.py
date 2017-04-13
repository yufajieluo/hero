#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2015 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import requires_csrf_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import time
import json
from hero.models import Article

from commResponse import CommResponse

class ArticleHandler(object):
    def __init__(self, request, LOG = None):
        self.request = request
        self.LOG = LOG
        self.rsp_handler = CommResponse()
        return

    '''
    def all_article(self):
        articles = Article.objects().order_by('+creat_time').exclude('content')
        article_instances = json.loads(articles.to_json())
        rsp_body = {'rsp_body': {'articles': article_instances}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp
    '''

    def all_article(self, page, title):
        if not title:
            articles = Article.objects.values('title', 'author', 'create_time').order_by('-create_time')
        else:
            articles = Article.objects.filter(title__contains = title).values('title', 'author', 'create_time').order_by('-create_time')
        paginator = Paginator(articles, 20)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        rsp_body = {'rsp_body': {'articles': contacts}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def get_article(self, title):
        article = Article.objects.get(title = title)
        if not article:
            pass
        rsp_body = {'rsp_body': {'article': article.to_json()}}
        rsp_body['rsp_body']['article']['content'] = rsp_body['rsp_body']['article']['content'].split('\r\n')
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp
