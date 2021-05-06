import uuid

from django.core.mail import send_mail

from users.models import EmailVerifyCode
# from random import choice
from random import randrange
from GuLiEdu.settings import EMAIL_FROM


# 产生随机验证码
def get_random_code(code_length):
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        # 随机选择一个字符
        # code += choice(code_source)
        code_str = code_source[randrange(0, len(code_source)-1)]
        code += code_str

    return code

def get_uuid():
    return uuid.uuid4()

# 发送邮箱验证码
def send_email_code(email, send_type):
    # 第一步：创建邮箱验证码对象，保存至数据库，用来以后做对比
    code = get_uuid()
    a = EmailVerifyCode()
    a.email = email
    a.send_type = send_type
    a.code = code
    a.save()
    # 第二步：发送邮件
    send_title = ''
    send_body = ''
    if send_type == 1:
        send_title = '欢迎注册谷粒教育网站'
        send_body = '请点击以下链接进行激活您的账号：\n http://127.0.0.1:8000/users/user_active/' + str(code)
        try:
            send_mail(send_title, send_body, EMAIL_FROM, [email])
            return True
        except:
            return False
    if send_type == 2:
        send_title = '谷粒教育重置密码'
        send_body = '请点击以下链接进行重置您的账号密码：\n http://127.0.0.1:8000/users/user_reset/' + str(code)
        try:
            send_mail(send_title, send_body, EMAIL_FROM, [email])
            return True
        except:
            return False
    if send_type == 3:
        send_title = '重新绑定邮箱'
        send_body = '验证码:\n' + str(code)
        try:
            send_mail(send_title, send_body, EMAIL_FROM, [email])
            return True
        except:
            return False
