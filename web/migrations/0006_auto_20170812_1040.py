# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 10:40
from __future__ import unicode_literals

from django.db import migrations, models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20170811_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='doc',
            field=models.ImageField(upload_to=web.models.path_rename),
        ),
    ]
