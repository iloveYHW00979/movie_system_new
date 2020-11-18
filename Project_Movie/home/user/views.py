from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from Project_Movie.Util.serializers import UserSerializer
from Project_Movie.Util.utils import response_failure, response_success
from Project_Movie.home.cinema.models import Order
from Project_Movie.home.user.models import *

class UserInfoView(APIView):

    def get(self, request):
        """进入用户个人信息界面"""
        user_id = request.query_params.get('id')  # 登录用户
        try:
            user = User.objects.filter(id=user_id).first()
            if user:
                serializer = UserSerializer(user)
                data = serializer.data
                if user.user_name == 'admin':
                    data = {
                        "roles":['admin'],
                        "data":serializer.data
                    }

            else:
                return response_failure('没有该id的用户')
        except Exception as e:
            raise e
        return response_success(code=200, data=data)

    def put(self, request):
        """更新用户信息"""
        query_params = request.data
        user_id = query_params.get('id')
        password = query_params.get('password')
        if password == '':
            return response_failure('密码不能为空')
        try:
            user_info = User.objects.filter(id=user_id).first()
            if user_info:
                serializer = UserSerializer(user_info, request.data)
                if serializer.is_valid():
                    serializer.save()
            else:
                return response_failure('没有该用户id')
        except Exception as e:
            raise e
        return response_success(code=200)

    def delete(self, request):
        """删除用户信息"""
        user_id = request.data.get('id')
        if user_id:
            try:
                user_info = User.objects.filter(id=user_id)
                order = Order.objects.filter(user_id=user_id)
                if user_info:
                    user_info.delete()
                else:
                    return response_failure('没有该用户id')
                if order:
                    order.delete()
                return response_success(code=200)
            except:
                return response_failure('数据库操作错误:没有该用户')

class UserOrderView(APIView):

    def get(self, request):
        """进入用户订单界面"""
        pass











