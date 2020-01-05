from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from common import stat

class AuthMiddleware(MiddlewareMixin):
# 登录检查中间件


    # 设置一个白名单，因为中间件对所有函数都生效，有不需要中间件的函数
    white_list = (
        '/api/user/get_vcode',
        '/api/user/submit_vcode',
    )

    def process_request(self,request):
        # 检查当前请求路径是否在‘白名单’中
        if request.path in self.white_list:
            return
        uid = request.session.get('id')
        if not uid:
            return JsonResponse({'code':stat.LOGIN_REQUIRED,'data':None})