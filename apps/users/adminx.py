import xadmin
from users.models import BannerInfo, EmailVerifyCode


class BannerInfoXadmin(object):
    list_display = ['image', 'url', 'add_time']
    list_filter = ['image', 'url']
    model_icon = 'fa fa-picture-o'


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']
    search_fields = ['code', 'email']
    model_icon = 'fa fa-envelope-o'


xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)