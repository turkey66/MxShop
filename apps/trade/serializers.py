# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/12/26 12:01'

from random import Random
import time

from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_pub_key_path

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False,)
    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 当前的用户
    add_time = serializers.DateTimeField(read_only=True,
                                         format='%Y-%m-%d %H:%M')
    nums = serializers.IntegerField(required=True, min_value=1, max_value=9999,
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "max_value": "商品数量不能大于9999",
                                        "required": "nums必填"
                                    })

    # 用serializer 外键关联
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):   # serializer 使用时，需要自己编写create方法
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"] # 这里的goods已经被反序列化成goods的对象了

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed


    # serializer,需要自己重写create update的方法，delete不用
    # modelserializer 已经帮我们重写好了

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 当前的用户
    pay_status = serializers.CharField(read_only=True)  # 只读
    order_sn = serializers.CharField(read_only=True)  # 只读
    trade_no = serializers.CharField(read_only=True)  # 只读
    pay_time = serializers.DateTimeField(read_only=True)  # 只读
    add_time = serializers.DateTimeField(read_only=True)  # 只读
    alipay_url = serializers.SerializerMethodField(read_only=True) # 只读

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016092400586721",
            app_notify_url="http://120.78.193.99:8000/alipay/return",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.193.99:8000/alipay/return"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(
            data=url)

        return re_url

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)  # 只读

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016092400586721",
            app_notify_url="http://120.78.193.99:8000/alipay/return",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.193.99:8000/alipay/return"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(
            data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
