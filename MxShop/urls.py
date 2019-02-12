"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve   # 专门处理静态文件
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView

from goods.views import GoodsListViewSet, CategoryViewset, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewSet, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset, AlipayView

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods") # 配置Goods的url
router.register(r'code', SmsCodeViewSet, base_name="code")
router.register(r'users', UserViewset, base_name="users")
router.register(r'categorys', CategoryViewset, base_name="categorys") # 配置Category的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs") # 配置userfavs的url
router.register(r'messages', LeavingMessageViewset, base_name="messages") # 配置messages的url
router.register(r'address', AddressViewset, base_name="address") # 配置address的url
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts") # 配置shopcarts的url
router.register(r'orders', OrderViewset, base_name="orders") # 配置orders的url
router.register(r'banners', BannerViewset, base_name="banners") # 配置banners的url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods") # 配置banners的url

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # 登录的配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),# 配置上传文件的访问处理函数
    url(r'^docs/', include_docs_urls(title="生鲜api")),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),#drf自带的token认证模式
    url(r'^login/$', obtain_jwt_token),#jwt的认证接口
    url(r'^alipay/return/', AlipayView.as_view(), name="alipay"),#jwt的认证接口
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    url('', include('social_django.urls', namespace='social'))  # 第三方登录
]