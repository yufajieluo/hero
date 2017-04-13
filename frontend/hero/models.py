from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    account = models.CharField(max_length = 128, primary_key = True, db_index = True)
    password = models.CharField(max_length = 128)
    username = models.CharField(max_length = 128)
    phone = models.CharField(max_length = 128)
    create_time = models.CharField(max_length = 19)
    last_time = models.CharField(max_length = 19)
    status = models.CharField(max_length = 32)
    role = models.CharField(max_length = 256)
    class Meta:
        db_table = 'user'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        data = {}
        for attr in fields:
            data[attr] = getattr(self, attr)
        return data

class Role(models.Model):
    name = models.CharField(max_length = 128, primary_key = True, db_index = True)
    level = models.IntegerField()
    description = models.CharField(max_length = 128)
    permissions = models.CharField(max_length = 256)
    users = models.CharField(max_length = 256)
    class Meta:
        db_table = 'role'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        data = {}
        for attr in fields:
            data[attr] = getattr(self, attr)
        return data

class Permission(models.Model):
    name = models.CharField(max_length = 128, primary_key = True, db_index = True)
    description = models.CharField(max_length = 128)
    url = models.CharField(max_length = 128)
    superior = models.CharField(max_length = 128)
    index = models.CharField(max_length = 8)
    class Meta:
        db_table = 'permission'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        data = {}
        for attr in fields:
            data[attr] = getattr(self, attr)
        return data

class Syslog(models.Model):
    time = models.CharField(max_length = 19, db_index = True)
    operation = models.CharField(max_length = 128)
    user = models.CharField(max_length = 128)
    addr = models.CharField(max_length = 128)
    class Meta:
        db_table = 'syslog'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        data = {}
        for attr in fields:
            data[attr] = getattr(self, attr)
        return data

class Article(models.Model):
    title = models.CharField(max_length = 128, primary_key = True, db_index = True)
    author = models.CharField(max_length = 128)
    create_time = models.CharField(max_length = 19, db_index = True)
    content = models.TextField()
    class Meta:
        db_table = 'article'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        data = {}
        for attr in fields:
            data[attr] = getattr(self, attr)

        return data

class Picture(models.Model):
    title = models.CharField(max_length = 128, primary_key = True, db_index = True)
    author = models.CharField(max_length = 128)
    create_time = models.CharField(max_length = 19, db_index = True)
    paths = models.TextField()
    class Meta:
        db_table = 'picture'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        data = {}
        for attr in fields:
            data[attr] = getattr(self, attr)

        return data

class Offset(models.Model):
    type = models.CharField(max_length = 32, primary_key = True)
    href = models.CharField(max_length = 256)
    class Meta:
        db_table = 'offset'
