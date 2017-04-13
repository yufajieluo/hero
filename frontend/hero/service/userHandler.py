#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2015 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from django.core.mail import send_mail
from django.views.decorators.csrf import requires_csrf_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import time
import json
from hero.models import User, Role, Permission, Syslog

from commCrypt import CryptHandler
from commRandom import RandomHandler
from commResponse import CommResponse

class UserHandler(object):
    def __init__(self, request, LOG = None):
        self.request = request
        self.LOG = LOG
        self.rsp_handler = CommResponse()
        self.crypt_handler = CryptHandler()
        self.random_handler = RandomHandler()
        return

    def get_captcha(self, account):
        if not account:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp

        user = User.objects.filter(account = account).only('account')
        if user:
            rsp = self.rsp_handler.generate_rsp_msg(21001, None)
            return rsp

        captcha = self.random_handler.generate_code()
        key = 'register:captcha:%s' % account
        cache.set(key, captcha)
        self.LOG.debug('account is {0}'.format(account))
        send_mail(
            settings.MAIL_SUBJECT_REGISTER,
            'The captcha code you register Hero is: [%s]' % captcha,
            settings.DEFAULT_FROM_EMAIL,
            [account],
            fail_silently = False
        )
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def register(self, account, password, fullname, phone, captcha):
        if not account or not password or not fullname or not phone or not captcha:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        user = User.objects.filter(account = account).only('account')
        if user:
            rsp = self.rsp_handler.generate_rsp_msg(21001, None)
            return rsp
        key = 'register:captcha:%s' % account
        if cache.get(key) != captcha:
            rsp = self.rsp_handler.generate_rsp_msg(21002, None)
            return rsp
        cache.delete(key)

        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        user = User(account = account, password = self.crypt_handler.encrypt(password), username = fullname, phone = phone, create_time = now_time)
        user.save()

        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def login(self, account, password, uuid):
        if not account or not password or not uuid:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        users = User.objects.filter(account = account)
        if not users:
            rsp = self.rsp_handler.generate_rsp_msg(21003, None)
            return rsp
        user = users[0]

        # check session
        if self.request.session.get('user_uuid', default = None):
            del self.request.session['user_uuid']
            del self.request.session['user_name']
            del self.request.session['user_account']

        if user.password != self.crypt_handler.encrypt(password):
            rsp = self.rsp_handler.generate_rsp_msg(21004, None)
            return rsp

        self.request.session['user_uuid'] = uuid
        self.request.session['user_name'] = user.username
        self.request.session['user_account'] = user.account
        user.status = 'login'
        user.last_time = time.strftime('%Y-%m-%d %H:%M:%S')
        user.save()

        permissions_instances = []
        if user.role:
            roles = Role.objects.filter(name = user.role)
            if roles:
                role = roles[0]
                if role.permissions:
                    self.LOG.debug(role.permissions.split(','))
                    permissions = Permission.objects.filter(name__in = role.permissions.split(',')).order_by('index')
                    permissions_instances = self.generate_permission_tree(permissions)
        rsp_body = {'rsp_body': {'permissions': permissions_instances}}
        self.LOG.debug('rsp_body is {0}'.format(rsp_body))
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def modify_password(self, account, old_password, new_password):
        if not account:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        users = User.objects.filter(account = account)
        if not users:
            rsp = self.rsp_handler.generate_rsp_msg(21003, None)
            return rsp
        user = users[0]
        if user.password != self.crypt_handler.encrypt(old_password):
            rsp = self.rsp_handler.generate_rsp_msg(21005, None)
            return rsp
        user.password = self.crypt_handler.encrypt(new_password)
        user.save()
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def reset_password(self, account):
        if not account:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        users = User.objects.filter(account = account)
        if not users:
            rsp = self.rsp_handler.generate_rsp_msg(21003, None)
            return rsp
        user = users[0]

        new_password = self.random_handler.generate_code()
        user.password = self.crypt_handler.encrypt(new_password)
        user.save()
        send_mail(
            settings.MAIL_SUBJECT_RESETPASS,
            'Your new password is: [%s]' % new_password,
            settings.MAIL_OUTBOX,
            [account],
            fail_silently = False
        )
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def logout(self):
        users = User.objects.filter(account = self.request.session['user_account'])
        user = users[0]
        user.status = 'logout'
        user.save()
        del self.request.session['user_uuid']
        del self.request.session['user_name']
        del self.request.session['user_account']
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp


    def all_roles(self):
        roles = Role.objects.all().order_by('level')
        role_instances = []
        for role in roles:
            role_instances.append(role)
        rsp_body = {'rsp_body': {'roles': role_instances}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def get_role(self, role_name):
        roles = Role.objects.filter(name = role_name).order_by('level')
        if not roles:
            rsp = self.rsp_handler.generate_rsp_msg(22002, None)
            return rsp
        role = roles[0]
        role_instance = role.to_json()
        role_instance['users'] = role_instance['users'].replace(',', '\n')
        role_instance['permissions'] = role_instance['permissions'].replace(',', '\n')
        rsp_body = {'rsp_body': {'role': role_instance}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def all_users(self):
        users = User.objects.all().values('account', 'username', 'phone', 'create_time', 'last_time', 'role')
        user_instances = []
        for user in users:
            user_instances.append(user)
        rsp_body = {'rsp_body': {'users': user_instances}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def get_user(self, account):
        if not account:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        users = User.objects.filter(account = account)
        if not users:
            rsp = self.rsp_handler.generate_rsp_msg(21003, None)
            return rsp
        user = users[0]
        user_instance = user.to_json()

        roles = Role.objects.order_by('level').values('name', 'level')
        role_instances = []
        for role in roles:
            role_instances.append(role)

        rsp_body = {'rsp_body': {'user': user_instance, 'roles': role_instances}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def modify_user(self, account, role_name):
        if not account:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        users = User.objects.filter(account = account)
        if not users:
            rsp = self.rsp_handler.generate_rsp_msg(21003, None)
            return rsp
        user = users[0]

        if user.role != role_name:
            old_role = user.role
            user.role = role_name
            user.save()

            roles = Role.objects.filter(name = old_role)
            if roles:
                role = roles[0]
                role_users = role.users.split(',')
                role_users.remove(account)
                role.users = ','.join(role_users)
                role.save()

            if role_name:
                roles = Role.objects.filter(name = role_name)
                if not roles:
                    rsp = self.rsp_handler.generate_rsp_msg(22002, None)
                    return rsp
                role = roles[0]
                if role.users:
                    if account not in role.users.split(','):
                        role_users = role.users.split(',')
                        role_users.append(account)
                        role.users = ','.join(role_users)
                else:
                    role.users = account
                role.save()

        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def all_permissions(self):
        permissions = Permission.objects.all().order_by('index')
        permissions_instances = []
        for permission in permissions:
            permissions_instances.append(permission)
        rsp_body = {'rsp_body': {'permissions': permissions_instances}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def get_permission(self, permission_name):
        permissions = Permission.objects.filter(name = permission_name)
        if not permissions:
            rsp = self.rsp_handler.generate_rsp_msg(22002, None)
            return rsp
        permission = permissions[0]
        permission_instance = permission.to_json()

        root_permissions = Permission.objects.filter(superior = 'ROOT').order_by('index')
        permission_instance['root_permissions'] = [permission.name for permission in root_permissions]

        rsp_body = {'rsp_body': {'permission': permission_instance}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def create_permission(self, name, desc, url, superior):
        if not name:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        permissions = Permission.objects.filter(name = name)
        if permissions:
            rsp = self.rsp_handler.generate_rsp_msg(22001, None)
            return rsp

        index = None
        if superior == 'ROOT':
            permissions = Permission.objects.filter(superior = superior).order_by('-index')
            if permissions:
                index = str(int(permissions[0].index) + 1)
            else:
                index = '0'
        else:
            permissions = Permission.objects.filter(superior = superior).order_by('-index')
            if not permissions:
                permissions = Permission.objects.filter(name = superior)
                index = str(float(permissions[0].index) + 0.1)
            else:
                index = str(float(permissions[0].index) + 0.1)

        permission = Permission(
            name = name,
            description = desc,
            url = url,
            superior = superior,
            index = index
        )
        permission.save()
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def modify_permission(self, name, desc, url, superior):
        if not name:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        permissions = Permission.objects.filter(name = name)
        if not permissions:
            rsp = self.rsp_handler.generate_rsp_msg(22002, None)
            return rsp
        permission = permissions[0]
        permission.description = desc
        permission.url = url
        permission.superior = superior
        permission.save()
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def remove_permission(self, name):
        if not name:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
            return rsp
        permissions = Permission.objects.filter(name = name)
        if not permissions:
            rsp = self.rsp_handler.generate_rsp_msg(22002, None)
            return rsp
        permission = permissions[0]
        permission.delete()

        roles = Role.objects.all()
        for role in roles:
            role_permissions = role.permissions.split(',')
            if name in role_permissions:
                role_permissions.remove(name)
                role.permissions = ','.join(role_permissions)
                role.save()
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def all_resources(self, group_name = None):
        permissions = Permission.objects.filter(superior = 'ROOT').order_by('name')
        permissions_instances = []
        for permission in permissions:
            permissions_instances.append(permission.to_json())

        rsp_body = {
            'rsp_body': {
                'permissions': permissions_instances,
            }
        }
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def get_role_permission(self, role_name):
        roles = Role.objects.filter(name = role_name)
        if not roles:
            rsp = self.rsp_handler.generate_rsp_msg(22002, None)
            return rsp
        role = roles[0]

        permissions = Permission.objects.all().order_by('index')
        permissions_instances = self.generate_permission_tree(permissions, role_permissions_list = role.permissions)
        rsp_body = {'rsp_body': {'permissions': permissions_instances}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def modify_role_permission(self, role_name, permissions):
        roles = Role.objects.filter(name = role_name)
        if not roles:
            rsp = self.rsp_handler.generate_rsp_msg(22002, None)
            return rsp
        role = roles[0]
        role.permissions = '' if not permissions else ','.join(permissions)
        role.save()
        rsp = self.rsp_handler.generate_rsp_msg(200, None)
        return rsp

    def generate_permission_tree(self, permission_objects, role_permissions_list = None):
        if not role_permissions_list:
            role_permissions_list = []
        permissions_instances = [
            {
                'name': permission_object.name,
                'url': permission_object.url,
                'open': True,
                'checked': True if permission_object.name in role_permissions_list else False,
                'children': []
            } for permission_object in permission_objects if permission_object.superior == 'ROOT'
        ]

        # 权限只有两层深度, 懒得写递归
        for permission_instance in permissions_instances:
            permission_instance['children'] = [
                {
                    'name': permission_object.name,
                    'url': permission_object.url,
                    'open': True,
                    'checked': True if permission_object.name in role_permissions_list else False,
                } for permission_object in permission_objects if permission_object.superior == permission_instance['name']
            ]
        return permissions_instances

    def all_logs(self, page):
        syslogs = Syslog.objects.values('time', 'operation', 'user', 'addr').order_by('-time')
        paginator = Paginator(syslogs, 20)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        rsp_body = {'rsp_body': {'logs': contacts}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp
