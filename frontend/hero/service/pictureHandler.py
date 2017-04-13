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
from hero.models import Picture

from commResponse import CommResponse

class PictureHandler(object):
    def __init__(self, request, LOG = None):
        self.request = request
        self.LOG = LOG
        self.rsp_handler = CommResponse()
        return

    def all_picture(self, page, title):
        if not title:
            pictures = Picture.objects.values('title', 'author', 'create_time').order_by('-create_time')
        else:
            pictures = Picture.objects.filter(title__contains = title).values('title', 'author', 'create_time').order_by('-create_time')
        paginator = Paginator(pictures, 20)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        rsp_body = {'rsp_body': {'pictures': contacts}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def get_picture(self, title):
        picture = Picture.objects.get(title = title)
        if not picture:
            pass
        rsp_body = {'rsp_body': {'picture': picture.to_json()}}
        rsp_body['rsp_body']['picture']['paths'] = rsp_body['rsp_body']['picture']['paths'].replace(settings.MEDIA_ROOT, '/static/media').split(',')
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp
