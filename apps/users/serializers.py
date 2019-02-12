# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/12/23 18:15'

import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

user_model = get_user_model()


class SmsSerializer(serializers.Serializer):
    # 这里没有用model serializer是因为code是必填的，前端并没有传递此

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号
        :param mobile:
        :return:
        """

        # 手机是否注册
        if user_model.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("=用户已经存在=")

        # 手机是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("=手机号错误=")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1,
                                                     seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago,
                                     mobile=mobile).count():
            raise serializers.ValidationError("=距离上一次发送未超过60秒=")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4, write_only=True,label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "缺少code",
                                     "max_length": "验证码错误",
                                     "min_length": "验证码错误"
                                 },
                                 help_text="验证码")  # user的model没有code字段，所以自己加上
    username = serializers.CharField(required=True, allow_blank=False, label="用户名", help_text="用户名",
                                     validators=[UniqueValidator(
                                         queryset=user_model.objects.all(), message="用户已存在~")])

    password = serializers.CharField(write_only=True, help_text="密码",
        style={'input_type': 'password'},label="密码"
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(
            mobile=self.initial_data["username"]).order_by("add_time")

        if verify_records:
            last_record = verify_records[0]

            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5,
                                                          seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")  # 找不到该手机的验证码

    def validate(self, attrs):  # 所有的validate执行完之后再执行这个，attrs 是所有字段的dict
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    # 改用信号通知的方法
    # def create(self, validated_data):
    #     user = super().create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    class Meta:
        model = user_model
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = user_model
        fields = ("name", "gender", "birthday", "mobile", "email")
