import redis
from django.shortcuts import render
from django.views import View
# Create your views here.
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
from .constants import IMAGE_CODE_EXPIRE_TIME,SMS_CODE_EXPIRE_TIME
from utils.response_code import RETCODE
from libs.yuntongxun.sms import CCP
class ImageCodeView(View):
    def get(self,request,uuid):
        text,image=captcha.generate_captcha()
        redis_Conn=get_redis_connection('code')
        redis_Conn.setex('img_%s'%uuid,IMAGE_CODE_EXPIRE_TIME,text)
        return http.HttpResponse(image,content_type='image/jpeg')

class SmsCodeView(View):
    def get(self,request,mobile):
        image_code=request.GET.get('imagecode')
        uuid=request.GET.get('uuid')
        if not all([mobile,image_code,uuid]):
            return http.JsonResponse({'code':RETCODE.NECESSARYPARAMERR,'errormsg':'参数不齐'})
        redis_conn=get_redis_connection('code')
        redis_code=redis_conn.get('img_%s'%mobile)
        if redis_code is None:
            return http.JsonResponse({'code':RETCODE.Timeout,'errmsg':'验证码过期'})
        if redis_code!=image_code:
            return  http.JsonResponse({'code':RETCODE.SMSCODERR,'errmsg':'图片验证码错误'})
        from random import randint
        sms_code=randint(1000,9999)
        redis_conn.setex('sms_%s'%mobile,SMS_CODE_EXPIRE_TIME,sms_code)
        CCP().send_template_sms(mobile,[sms_code,5],1)
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})


