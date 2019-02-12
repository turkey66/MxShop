from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderGoods, OrderInfo
from utils.alipay import AliPay
from MxShop.settings import ali_pub_key_path, private_key_path

# Create your views here.


class ShoppingCartViewset(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 用户登录验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = "goods_id" # 查询字段，默认是id,更新也是这个字段

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def perform_create(self, serializer):
        # 添加购物车时，商品的库存数量减少
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        # 删除购物车商品时，增加库存量
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        # 修改购物车商品数量时，更新库存数量
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_num = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_num
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()



class OrderViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 用户登录验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer
    #lookup_field = "order_sn"  # 查询字段，默认是id,更新也是这个字段

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save() # 提交购买后，生成order，订单编号在serializer里面已经生成

        # 取出用户购物车的商品，添加到订单的商品表，然后删除购物车的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()

        return order


class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)  # 字典弹出签名

        alipay = AliPay(
            appid="2016092400586721",
            app_notify_url="http://120.78.193.99:8000/alipay/return",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.193.99:8000/alipay/return"
        )

        verify_res = alipay.verify(processed_dict, sign)  # 验证ali 的签名

        if verify_res:
            # 支付宝的签名验证通过，去修改订单的信息
            # order_sn = processed_dict.get('out_trade_no', None)
            # trade_no = processed_dict.get('trade_no', None)
            # trade_status = processed_dict.get('trade_status', None)
            #
            # existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            # if existed_orders:
            #     for existed_order in existed_orders:
            #         existed_order.pay_status = trade_status
            #         existed_order.trade_no = trade_no
            #         existed_order.pay_time = datetime.now()
            #         existed_order.save()
            #
            #     return Response("success")
            # 这里不用再改库里的信息了，一个notify已经改了

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=2)
            return response
        else:
            print("没有该订单！")
            response = redirect("index")
            return response


    def post(self, request):
        """
        处理支付宝notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None) # 字典弹出签名

        alipay = AliPay(
            appid="2016092400586721",
            app_notify_url="http://120.78.193.99:8000/alipay/return",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://120.78.193.99:8000/alipay/return"
        )

        verify_res = alipay.verify(processed_dict, sign)    # 验证ali 的签名

        if verify_res:
            # 支付宝的签名验证通过，去修改订单的信息
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            if existed_orders:

                for existed_order in existed_orders:
                    # 支付成功之后，更改商品的售卖数量
                    order_goods = existed_order.goods.all()
                    for order_good in order_goods: # 所有订单的商品详情
                        goods = order_good.goods   #售卖的商品
                        goods.sold_num += order_good.goods_num
                        goods.save()

                    #支付成功之后，更改订单的状态
                    existed_order.pay_status = trade_status
                    existed_order.trade_no = trade_no
                    existed_order.pay_time = datetime.now()
                    existed_order.save()

                return Response("success")
            else:
                print("没有该订单！")