# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-04-21 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techpedia', '0002_auto_20170421_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
