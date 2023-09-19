import redis
from django.shortcuts import render
from django.views import View
# Create your views here.
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
from .constants import IMAGE_CODE_EXPIRE_TIME
class ImageCodeView(View):
    def get(self,request,uuid):
        text,image=captcha.generate_captcha()
        redis_Conn=get_redis_connection('code')
        redis_Conn.setex('img_%s'%uuid,IMAGE_CODE_EXPIRE_TIME,text)
        return http.HttpResponse(image,content_type='image/jpeg')