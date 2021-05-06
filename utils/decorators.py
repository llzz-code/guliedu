from django.http import JsonResponse
from django.shortcuts import redirect, reverse


def login_decorator(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return JsonResponse({'status': 'nologin'})

            # 拿到目前访问的完整url
            url = request.get_full_path()
            ret = redirect(reverse('users:user_login'))
            ret.set_cookie('url', url)
            return ret
    return inner