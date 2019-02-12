# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-09 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20181209_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategory',
            name='category_type',
            field=models.CharField(choices=[('1', '一级类目'), ('2', '二级类目'), ('3', '三级类目')], help_text='类目级别', max_length=10, verbose_name='类目级别'),
        ),
    ]
