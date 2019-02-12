from random import choice

from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from MxShop.settings import APIKEY
from .models import VerifyCode

user_model = get_user_model()

# Create your views here.
class CustomBackend(ModelBackend): #重写认证方法
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = user_model.objects.get(Q(username=username)|Q(mobile=username)) # |或  ,和
            if user.check_password(password):   # 不能直接从库里验证密码，库密码被加密了的
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    #重新create的方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]    # 获取mobile的值
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()  # 短信发送成功验证码保存到库里面
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = [choice(seeds) for _ in range(4)]
        return "".join(random_str)


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)    # 加Session为了在api时调试方便

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)  #先拿到保存user，并拿到user

        payload = jwt_payload_handler(user)
        re_dict = serializer.data
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()    # 返回这个user ，为了和token做关联

    def get_object(self):
        # 用delete方法的时候，或者retrive详情时，update更新，会调用该方法
        return self.request.user

    # 重写，自定鉴权，只在retrive时，判断用户是否有登录
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    # 重写获取serializer_class，需要根据不同情况返回不同的serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer