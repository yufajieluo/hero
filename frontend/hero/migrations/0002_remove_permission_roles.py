# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 02:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='roles',
        ),
    ]
