from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMidware(MiddlewareMixin):
    # 中间件1
    def process_request(self, request):
        # 如果没有返回值，那么就默认返回NULL，默认继续往后走
        # 如果有返回值，可以返回render或者httpresponse
        # 排除那些不需要确认登录就可以通过的url
        if request.path_info in ["/login/","/image/code/","/test/"]:
            return
        # 读取session信息，能读到，则返回none。如果没有读到，返回登录界面
        info_dict = request.session.get("info")
        if info_dict:
            return None
        return redirect("/login/")
