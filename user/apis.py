from django.http import JsonResponse
from django.core.cache import cache
from user.models import User
from user import logics
from user.logics import send_sms
from common import stat

def get_vcode(request):
    # 用户获取验证码
    phonenum = request.GET.get('phonenum')

    success = logics.send_sms(phonenum)

    if success:
        return JsonResponse({'code':stat.OK,'data':None})
    else:

        return JsonResponse({'code':stat.SMS_ERR,'data':None})

def submit_vcode(request):
    '''检查短信验证码，同时进行登陆或者注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    #print(phonenum)
    key = 'Vcode-%s' % phonenum
    print(key)
    print(type(key))
    cached_vcode = cache.get(key)
    print(cached_vcode)
    if vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)  # 获取用户
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)  # 创建新用户

        # 记录用户登陆状态
        request.session['uid'] = user.id
        return JsonResponse({'code': stat.OK, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def get_profile(request):
    # 获取个人资料
    uid = request.session.get('id')
    if uid:
        user = User.objects.get(id=uid)
    else:
        return JsonResponse({'code':1002,'data':''})

def set_profile(request):
    # 修改个人资料
    uid = request.session['id']
    user = User.objects.get(id=uid)
    return JsonResponse({})

def upload_avatar(request):
    # 头像上传
    uid = request.session['id']
    user = User.objects.get(id=uid)
    return JsonResponse({})
