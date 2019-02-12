from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

user_model = get_user_model() # 获取用户model
# Create your models here.


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(user_model, verbose_name="用户", help_text="用户id")
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods") # 联合唯一

    def __str__(self):
        return self.user.name + ",收藏"


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICE = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(user_model, verbose_name="用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICE, verbose_name="留言类型",
                                       help_text="留言类型：1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=30, default="", verbose_name="主题")
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(verbose_name="上传的文件", upload_to="user/file/", help_text="上传的文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)".format(self.user.name, self.subject)


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(user_model, verbose_name="用户")
    province = models.CharField(null=True, blank=True, max_length=20, default="", verbose_name="省份")
    city = models.CharField(null=True, blank=True, max_length=20, default="", verbose_name="城市")
    district = models.CharField(null=True, blank=True, max_length=20, default="", verbose_name="区域")
    address = models.CharField(max_length=50, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=10, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="手机号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,收货地址".format(self.user.name)