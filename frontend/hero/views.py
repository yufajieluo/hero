#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2017 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

import json
import time
import inspect
import logging
from service import commDecorator
from service import userHandler, articleHandler, pictureHandler

logger = logging.getLogger('django')
# Create your views here.

@commDecorator.login_required
@commDecorator.print_log(LOG = logger)
def welcome(request):
    resp_json = {
        'current_permission': json.dumps(request.session.get('current_permissions', {})),
        'user_name': request.session.get('user_name', None),
        'account': request.session.get('user_account', None)
    }
    return render_to_response('hero/welcome.html', resp_json)

@commDecorator.print_log(LOG = logger)
def captcha(request):
    context = {}
    if request.method == 'GET':
        account = request.GET.get('register_account', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.get_captcha(account)
    return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.print_log(LOG = logger)
def register(request):
    context = {}
    if request.method == 'POST':
        account = request.POST.get('register_account', None)
        password = request.POST.get('register_password', None)
        fullname = request.POST.get('fullname', None)
        phone = request.POST.get('phone', None)
        captcha = request.POST.get('captcha', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.register(account, password, fullname, phone, captcha)
        return HttpResponseRedirect('/hero/?request=%s&info=%s#signup' % (inspect.stack()[0][3], json.dumps(context['rsp_head'])))
    else:
        return HttpResponseRedirect('/hero/')

@commDecorator.print_log(LOG = logger)
def login(request):
    context = {}
    if request.method == 'POST':
        account = request.POST.get('login_account', None)
        password = request.POST.get('login_password', None)
        uuid = request.POST.get('login_uuid', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.login(account, password, uuid)
        if context['rsp_head']['rsp_code'] == 200:
            request.session['current_permissions'] = context['rsp_body']['permissions']
            return HttpResponseRedirect('/hero/user/welcome/')
        else:
            context = context['rsp_head']
            context['rsp_request'] = inspect.stack()[0][3]
            return render_to_response('hero/index.html', {'context': context})
    else:
        info = request.GET.get('info', None)
        request = request.GET.get('request', None)
        try:
            context = json.loads(info)
            context['rsp_request'] = request
        except:
            context = None
        return render_to_response('hero/index.html', {'context': context})

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def password(request):
    context = {}
    if request.method == 'POST':
        account = request.POST.get('account', None)
        old_password = request.POST.get('original_password', None)
        new_password = request.POST.get('new_password', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.modify_password(account, old_password, new_password)
    elif request.method == 'DELETE':
        request_delete = QueryDict(request.body)
        account = request_delete.get('account', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.reset_password(account)
    return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def logout(request):
    context = {}
    if request.method == 'POST':
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.logout()
    return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def role(request):
    context = {}
    if request.method == 'GET':
        role_name = request.GET.get('role_name', None)
        user_handler = userHandler.UserHandler(request, logger)
        if not role_name:
            context = user_handler.all_roles()
            resp_json = {
                'context': context,
                'current_permission': json.dumps(request.session.get('current_permissions', {})),
                'user_name': request.session.get('user_name', None),
                'account': request.session.get('user_account', None)
            }
            return render_to_response('hero/role.html', resp_json)
        else:
            context = user_handler.get_role(role_name)
            return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def user(request):
    context = {}
    if request.method == 'GET':
        user_account = request.GET.get('account', None)
        user_handler = userHandler.UserHandler(request, logger)
        if not user_account:
            context = user_handler.all_users()
            resp_json = {
                'context': context,
                'current_permission': json.dumps(request.session.get('current_permissions', {})),
                'user_name': request.session.get('user_name', None),
                'account': request.session.get('user_account', None)
            }
            return render_to_response('hero/user.html', resp_json)
        else:
            context = user_handler.get_user(user_account)
            return HttpResponse(json.dumps(context), content_type="application/json")

    elif request.method == 'POST':
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.modify_user(
            request.POST.get('user_account', None),
            request.POST.get('user_role', None)
        )
        return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def permission(request):
    context = {}
    if request.method == 'GET':
        permission_name = request.GET.get('permission_name', None)
        user_handler = userHandler.UserHandler(request, logger)
        if not permission_name:
            context = user_handler.all_permissions()
            resp_json = {
                'context': context,
                'current_permission': json.dumps(request.session.get('current_permissions', {})),
                'user_name': request.session.get('user_name', None),
                'account': request.session.get('user_account', None)
            }
            return render_to_response('hero/permission.html', resp_json)
        else:
            context = user_handler.get_permission(permission_name)
            return HttpResponse(json.dumps(context), content_type="application/json")
    elif request.method == 'PUT':
        request_put = QueryDict(request.body)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.create_permission(
            request_put.get('name', None),
            request_put.get('desc', None),
            request_put.get('url', None),
            request_put.get('superior', None),
        )
        return HttpResponse(json.dumps(context), content_type="application/json")
    elif request.method == 'POST':
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.modify_permission(
            request.POST.get('name', None),
            request.POST.get('desc', None),
            request.POST.get('url', None),
            request.POST.get('superior', None),
        )
        return HttpResponse(json.dumps(context), content_type="application/json")
    elif request.method == 'DELETE':
        request_delete = QueryDict(request.body)
        permission_name = request_delete.get('permission_name', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.remove_permission(permission_name)
        return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def role_permission(request):
    context = {}
    if request.method == 'GET':
        role_name = request.GET.get('role_name', None)
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.get_role_permission(role_name)
        return HttpResponse(json.dumps(context), content_type="application/json")
    elif request.method == 'POST':
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.modify_role_permission(
            request.POST.get('role_name', None),
            request.POST.getlist('permission', None)
        )
        return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def resource(request):
    context = {}
    if request.method == 'GET':
        user_handler = userHandler.UserHandler(request, logger)
        context = user_handler.all_resources()
        return HttpResponse(json.dumps(context), content_type="application/json")

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def restrict_article(request):
    context = {}
    if request.method == 'GET':
        title = request.GET.get('search_title', None)
        page = request.GET.get('page')
        article_handler = articleHandler.ArticleHandler(request, logger)
        context = article_handler.all_article(page, title)
        resp_json = {
            'context': context,
            'current_permission': json.dumps(request.session.get('current_permissions', {})),
            'user_name': request.session.get('user_name', None),
            'account': request.session.get('user_account', None)
        }
        return render_to_response('hero/restrict_article.html', resp_json)

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def restrict_article_content(request):
    context = {}
    if request.method == 'GET':
        title = request.GET.get('title', None)
        article_handler = articleHandler.ArticleHandler(request, logger)
        context = article_handler.get_article(title)
        resp_json = {
            'context': context,
            'current_permission': json.dumps(request.session.get('current_permissions', {})),
            'user_name': request.session.get('user_name', None),
            'account': request.session.get('user_account', None)
        }
        return render_to_response('hero/restrict_article_content.html', resp_json)

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def restrict_picture(request):
    context = {}
    if request.method == 'GET':
        title = request.GET.get('search_title', None)
        page = request.GET.get('page')
        picture_handler = pictureHandler.PictureHandler(request, logger)
        context = picture_handler.all_picture(page, title)
        resp_json = {
            'context': context,
            'current_permission': json.dumps(request.session.get('current_permissions', {})),
            'user_name': request.session.get('user_name', None),
            'account': request.session.get('user_account', None)
        }
        return render_to_response('hero/restrict_picture.html', resp_json)

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def restrict_picture_content(request):
    context = {}
    if request.method == 'GET':
        title = request.GET.get('title', None)
        picture_handler = pictureHandler.PictureHandler(request, logger)
        context = picture_handler.get_picture(title)
        resp_json = {
            'context': context,
            'current_permission': json.dumps(request.session.get('current_permissions', {})),
            'user_name': request.session.get('user_name', None),
            'account': request.session.get('user_account', None)
        }
        return render_to_response('hero/restrict_picture_content.html', resp_json)

@commDecorator.login_required
@commDecorator.logging_system
@commDecorator.print_log(LOG = logger)
def restrict_video(request):
    context = {}
    if request.method == 'GET':
        page = request.GET.get('page')
        resp_json = {
            'context': context,
            'current_permission': json.dumps(request.session.get('current_permissions', {})),
            'user_name': request.session.get('user_name', None),
            'account': request.session.get('user_account', None)
        }
        return render_to_response('hero/restrict_video.html', resp_json)

@commDecorator.login_required
@commDecorator.print_log(LOG = logger)
def log(request):
    context = {}
    if request.method == 'GET':
        page = request.GET.get('page')
        user_handler = userHandler.UserHandler(request)
        context = user_handler.all_logs(page)
    resp_json = {
        'context': context,
        'current_permission': json.dumps(request.session.get('current_permissions', {})),
        'user_name': request.session.get('user_name', None),
        'account': request.session.get('user_account', None)
    }
    return render_to_response('hero/log.html', resp_json)

def custom_page_not_found(request):
    resp_json = {
        'current_permission': json.dumps(request.session.get('current_permissions', {})),
        'user_name': request.session.get('user_name', None),
        'account': request.session.get('user_account', None)
    }
    return render_to_response('hero/404.html', resp_json)

def custom_error(request):
    return render_to_response('hero/500.html')


