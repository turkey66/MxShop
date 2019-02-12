# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/12/24 13:40'

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

user_model = get_user_model()

# 模块新建的时候，会执行该信号
@receiver(post_save, sender=user_model)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()