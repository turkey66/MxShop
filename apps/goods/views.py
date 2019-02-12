from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilter
# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    list:
        商品分类商品列表页，分页，搜索，过滤，排序
    retrieve:
        获取详情
    """
    queryset = Goods.objects.all()
    throttle_classes = (UserRateThrottle, AnonRateThrottle) # 配置api 访问频率
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        # 查看详情时会调方法，重写，让每次调详情的时候，点击数加一
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(CacheResponseMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    # mixins.RetrieveModelMixin 获取某个商品的详情
    # categorys/2
    """
    List:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewset(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer