# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/12/24 17:20'

from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 当前的用户

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        fields = ('user', 'goods', 'id')


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 当前的用户
    add_time = serializers.DateTimeField(read_only=True,
                                         format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = (
        "id", "user", "message_type", "subject", "message", "file", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 当前的用户
    add_time = serializers.DateTimeField(read_only=True,
                                         format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = (
            "id", 'user', "province", "city", "district", "address", "signer_name",
            "signer_mobile", "add_time")
