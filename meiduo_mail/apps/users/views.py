import http.client
import re
from .models import User

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import View
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        password2=data.get('password2')
        mobile=data.get('mobile')
        if not all([username,password,password2,mobile]):
            return HttpResponse('参数有问题')
        if not re.match(r'[0-9a-zA-Z_]{5,20}',username):
            return HttpResponse('用户名不符合规范',status=400)
        if not re.match(r'[0-9a-zA-Z_]{8,20}',password):
            return HttpResponse('密码不符合规范',status=400)
        if password!=password2:
            return HttpResponse('重复密码不符合规范',status=400)
        if not re.match(r'1[3-9]\d{9}',mobile):
            return HttpResponse('两次密码不一致',status=400)
        user=User.objects.create_user(username=username,password=password,mobile=mobile)
        return HttpResponse('注册成功！')






        #return HttpResponse("Post request received.")