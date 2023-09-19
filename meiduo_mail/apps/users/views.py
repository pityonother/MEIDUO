import http.client
import re
from .models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse

import logging
from django.views import View

logger=logging.getLogger('django')
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        password2=data.get('password2')
        mobile=data.get('mobile')
        allow=data.get('allow')
        print(type(allow))
        if not all([username,password,password2,mobile]):
            return HttpResponse('参数有问题')
        if not re.match(r'[0-9a-zA-Z_]{5,20}',username):
            return HttpResponse('用户名不符合规范',status=400)
        if not re.match(r'[0-9a-zA-Z_]{8,20}',password):
            return HttpResponse('密码不符合规范',status=400)
        if password!=password2:
            return HttpResponse('重复密码不符合规范',status=400)
        if not re.match(r'1[3-9]\d{9}',mobile):
            return HttpResponse('手机号不符合规则',status=400)
        if allow==None:
            return HttpResponse('请勾选用户使用协议',status=400)
        try:
            user=User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            logger.error(e)
            return HttpResponse(f'{e}',status=400)
        from django.contrib.auth import login
        login(request,user)
        return redirect(reverse('contents:index'))
class UsernameCountView(View):
    def get(self,request,username):
        try:
          count=User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400,'errmsg':'数据库异常'})
        return JsonResponse({'code':0,'count':count})









        #return HttpResponse("Post request received.")