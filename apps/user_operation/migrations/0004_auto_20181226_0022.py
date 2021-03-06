# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-12-26 00:22
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20181224_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='city',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='province',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='省份'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='district',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='区域'),
        ),
        migrations.AlterField(
            model_name='userfav',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='userfav',
            name='goods',
            field=models.ForeignKey(help_text='商品id', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='userfav',
            name='user',
            field=models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
