# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('title', models.CharField(db_index=True, max_length=128, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=128)),
                ('create_time', models.CharField(db_index=True, max_length=19)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Offset',
            fields=[
                ('type', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('href', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'offset',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('name', models.CharField(db_index=True, max_length=128, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=128)),
                ('superior', models.CharField(max_length=128)),
                ('index', models.CharField(max_length=8)),
                ('roles', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'permission',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('title', models.CharField(db_index=True, max_length=128, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=128)),
                ('create_time', models.CharField(db_index=True, max_length=19)),
                ('paths', models.TextField()),
            ],
            options={
                'db_table': 'picture',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('name', models.CharField(db_index=True, max_length=128, primary_key=True, serialize=False)),
                ('level', models.IntegerField()),
                ('description', models.CharField(max_length=128)),
                ('permissions', models.CharField(max_length=256)),
                ('users', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='Syslog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(db_index=True, max_length=19)),
                ('operation', models.CharField(max_length=128)),
                ('user', models.CharField(max_length=128)),
                ('addr', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'syslog',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('account', models.CharField(db_index=True, max_length=128, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=128)),
                ('create_time', models.CharField(max_length=19)),
                ('last_time', models.CharField(max_length=19)),
                ('status', models.CharField(max_length=32)),
                ('role', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
