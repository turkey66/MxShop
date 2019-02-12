from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserFavViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        创建fav
    delete:
        删除fav
    """
    # serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 用户登录验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"  # 查询字段，默认是id,更新也是这个字段

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

        # 重写获取serializer_class，需要根据不同情况返回不同的serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer

    # 收藏数加一，用信号量的方法来写
    # def perform_create(self, serializer):
    #     ins = serializer.save()
    #     goods = ins.goods
    #     goods.fav_num += 1
    #     goods.save()


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言功能
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 用户登录验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):#modelviewset集成了增删改查
    """
    收货地址管理
    list:
        获取用户地址
    create:
        添加地址
    delete:
        删除收货地址
    update:
        修改收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 用户登录验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
