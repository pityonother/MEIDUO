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
import logging
logger=logging.getLogger('django')
class ImageCodeView(View):
    def get(self,request,uuid):
        text,image=captcha.generate_captcha()
        redis_Conn=get_redis_connection('code')
        redis_Conn.setex('img_%s'%uuid,IMAGE_CODE_EXPIRE_TIME,text)
        return http.HttpResponse(image,content_type='image/jpeg')

class SmsCodeView(View):
    def get(self,request,mobile):
        image_code=request.GET.get('image_code')
        uuid=request.GET.get('image_code_id')
        if not all([mobile,image_code,uuid]):
            return http.JsonResponse({'code':RETCODE.NECESSARYPARAMERR,'errmsg':'参数不齐'})
        try:
            redis_conn=get_redis_connection('code')
            redis_code=redis_conn.get('img_%s'%uuid)
            if redis_code is None:
                return http.JsonResponse({'code':RETCODE.Timeout,'errmsg':'验证码过期'})
            redis_conn.delete('img_%s'%uuid)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':RETCODE.DBERR,'errmsg':'redis有异常'})
        if redis_code.decode().lower()!=image_code.lower():
            return  http.JsonResponse({'code':RETCODE.SMSCODERR,'errmsg':'图片验证码错误'})
        send_flag=redis_conn.get('send_flag_%s'%mobile)
        if send_flag:
            return http.JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'操作太频繁'})
        from random import randint
        sms_code=randint(1000,9999)
        pipe=redis_conn.pipeline()
        pipe.setex('sms_%s'%mobile,SMS_CODE_EXPIRE_TIME,sms_code)
        pipe.setex('send_flag_%s'%mobile,60,1)
        pipe.execute()
        #CCP().send_template_sms(mobile,[sms_code,5],1)
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code)
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})


