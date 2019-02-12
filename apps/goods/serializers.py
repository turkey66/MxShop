# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/12/2 17:41'

from rest_framework import serializers
from django.db.models import Q

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品类别3序列化
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品类别2序列化
    """
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品类别1序列化
    """
    sub_cat = GoodsCategorySerializer2(many=True) # many设置这个变量表示下面有很多个，不设置会报错
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化
    """
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    """
    首页轮播图序列化
    """
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    """
    品牌
    """
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField() # 自定义方法字段
    sub_cat = GoodsCategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = '{}'
        ad_goods= IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
            # context 返回的图片没有域名，要把这个加上
        return goods_json


    def get_goods(self, obj):
        all_goods = Goods.objects.filter(
            Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
                category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"


