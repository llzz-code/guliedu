from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator

from courses.models import CourseInfo
from operations.models import UserLove, UserMessage
from orgs.models import OrgInfo, TeacherInfo
from utils.send_mail_tool import send_email_code
# Create your views here.

from users.forms import UserRegisterForm, UserLoginForm, UserForgetForm, UserResetForm, \
    UserChangeImageForm, UserChangeInfoForm, UserChangeEmailForm, UserResetEmailForm, UserPwdForm
from users.models import UserProfile, EmailVerifyCode, BannerInfo

class IndexView(View):
    def get(self, request):
        all_banners = BannerInfo.objects.all().order_by('-add_time')[:5]
        course_banners = CourseInfo.objects.filter(is_banner=True)[:3]
        all_course = CourseInfo.objects.filter(is_banner=False)[:6]
        all_orgs = OrgInfo.objects.all().order_by('-love_num')[:15]
        return render(request, 'index.html', locals())


# def index(request):
#     all_banners = BannerInfo.objects.all().order_by('-add_time')[:5]
#     course_banners = CourseInfo.objects.filter(is_banner=True)[:3]
#     all_course = CourseInfo.objects.filter(is_banner=False)[:6]
#     all_orgs = OrgInfo.objects.all().order_by('-love_num')[:15]
#     return render(request, 'index.html', locals())

class RegisterView(View):
    def get(self, request):
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', locals())

    def post(self, request):
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'users/register.html', {
                    'msg': '用户已经存在'
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email

                # 进行邮箱验证激活
                # 发送邮箱验证码
                if send_email_code(email, 1):
                    a.save()
                    return HttpResponse('情尽快前往邮箱激活账号')
                else:
                    return HttpResponse('注册失败')
                # return redirect('/users/user_login')
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                if user.is_start:
                    login(request, user)
                    a = UserMessage()
                    a.message_man = user.id
                    a.message_content = '欢迎登录'
                    a.save()
                    url = request.COOKIES.get('url', '/')
                    ret = redirect(url)
                    ret.delete_cookie('url')
                    return ret
                else:
                    return HttpResponse('请去邮箱激活账号')
            else:
                return render(request, 'users/login.html', {
                    'msg': '邮箱或密码有误'
                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form
            })


def user_logout(request):
    logout(request)
    return redirect('/')


def user_active(request, code):
    if code:
        print(code)
        email_ver_list = EmailVerifyCode.objects.filter(code=code)
        if email_ver_list:
            print(email_ver_list)
            email_ver = email_ver_list[0]
            email = email_ver.email
            print(email)
            user_list = UserProfile.objects.filter(username=email)
            print(user_list)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect('/')
            else:
                return HttpResponse('code1')
        else:
            return HttpResponse('code2')
    else:
        return HttpResponse('code3')


class ForgetView(View):
    def get(self, request):
        user_forget_form = UserForgetForm()

        return render(request, 'users/forgetpwd.html', {
            'user_forget_form': user_forget_form
        })

    def post(self, request):
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                if send_email_code(email, 2):
                    return HttpResponse('情尽快去邮箱重置密码')
                else:
                    msg = '验证失败'
                    return render(request, 'users/forgetpwd.html', locals())
            else:
                msg = '用户不存在'
                return render(request, 'users/forgetpwd.html', locals())
        else:
            return render(request, 'users/forgetpwd.html', locals())


def user_reset(request, code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password_reset.html', {
                'code': code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password1 = user_reset_form.cleaned_data['password1']
                password2 = user_reset_form.cleaned_data['password2']
                if password1 == password2:
                    email_ver_list = EmailVerifyCode.objects.filter(code=code)
                    if email_ver_list:
                        email_ver = email_ver_list[0]
                        email = email_ver.email
                        user_list = UserProfile.objects.filter(email=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password1)
                            user.save()
                            return redirect('/users/user_login/')
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password_reset.html', {
                        'msg': '密码不一致',
                        'code': code
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'user_reset_form': user_reset_form
                })


def user_info(request):
    return render(request, 'users/usercenter-info.html')


def user_changeimage(request):
    # instance 指明实例是什么，作修改的时候需要知道是给哪个对象实例进行修改，如果不指明，将会被当做创建对象去保存
    user_changeimage_form = UserChangeImageForm(request.POST, request.FILES, instance=request.user)
    if user_changeimage_form.is_valid():
        user_changeimage_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail'})


def user_changeinfo(request):
    user_changeinfo_form = UserChangeInfoForm(request.POST, instance=request.user)
    if user_changeinfo_form.is_valid():
        user_changeinfo_form.save(commit=True)
        return JsonResponse({'status': 'ok', 'msg': '修改成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '修改失败'})


def user_changeemail(request):
    user_changeeamil_form = UserChangeEmailForm(request.POST)
    if user_changeeamil_form.is_valid():
        email = user_changeeamil_form.cleaned_data['email']
        user_list = UserProfile.objects.filter(Q(email=email) | Q(username=email))
        if user_list:
            return JsonResponse({'status': 'fail', 'msg': '邮箱已经被绑定'})
        else:
            email_ver_list = EmailVerifyCode.objects.filter(email=email, send_type=3)
            if email_ver_list:
                email_ver = email_ver_list.order_by('-add_time')[0]
                # 判断当前时间和最近添加验证码的时间之差
                if (datetime.now() - email_ver.add_time).seconds > 60:
                    email_ver.delete()
                    send_email_code(email, 3)
                    return JsonResponse({'status': 'ok', 'msg': '验证码已发送至邮箱'})
                else:
                    return JsonResponse({'status': 'fail', 'msg': '请去邮箱查看验证码或请一分钟后重新发送'})
            else:
                send_email_code(email, 3)
                return JsonResponse({'status': 'ok', 'msg': '验证码已发送至邮箱'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '您的邮箱存在异常'})


def user_resetemail(request):
    user_resetemail_form = UserResetEmailForm(request.POST)
    if user_resetemail_form.is_valid():
        email = user_resetemail_form.cleaned_data['email']
        code = user_resetemail_form.cleaned_data['code']
        print('==========', code, email)
        code_ver_list = EmailVerifyCode.objects.filter(email=email, code=code)
        print('-----------', code_ver_list)
        if code_ver_list:
            code_ver = code_ver_list[0]
            if (datetime.now() - code_ver.add_time).seconds < 60:
                request.user.username = email
                request.user.email = email
                request.user.save()
                return JsonResponse({'status': 'ok', 'msg': '修改成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '验证码已经失效，请重新获取验证码'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码错误'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码异常'})


def user_course(request):
    all_courses = request.user.usercourse_set.all()
    course_list = [usercourse.study_course for usercourse in all_courses]
    return render(request, 'users/usercenter-mycourse.html', locals())


def user_fav_org(request):
    # all_fav_org = request.user.userlove_set.all().filter(love_type=1)
    all_fav_org = UserLove.objects.filter(love_man=request.user, love_type=1, love_status=True)
    org_id_list = [user_fav.love_id for user_fav in all_fav_org]
    org_list = OrgInfo.objects.filter(id__in=org_id_list)
    return render(request, 'users/usercenter-fav-org.html', {
        'org_list': org_list
    })


def user_fav_teacher(request):
    all_fav_teacher = UserLove.objects.filter(love_man=request.user, love_type=3, love_status=True)
    teacher_id_list = [user_fav.love_id for user_fav in all_fav_teacher]
    teacher_list = TeacherInfo.objects.filter(id__in=teacher_id_list)
    return render(request, 'users/usercenter-fav-teacher.html', {
        'teacher_list': teacher_list
    })


def user_fav_course(request):
    all_fav_course = UserLove.objects.filter(love_man=request.user, love_type=2, love_status=True)
    course_id_list = [user_fav.love_id for user_fav in all_fav_course]
    course_list = CourseInfo.objects.filter(id__in=course_id_list)
    return render(request, 'users/usercenter-fav-course.html', {
        'course_list': course_list
    })


def user_message(request):
    msg_list = UserMessage.objects.filter(message_man=request.user.id).order_by('-add_time')
    page = request.GET.get('page', 1)
    pages = Paginator(msg_list, 5)
    try:
        pager = pages.page(page)
    except:
        pager = pages.page(1)
    return render(request, 'users/usercenter-message.html', locals())


def user_message_read(request):
    read_id = request.GET.get('read_id', '')
    msg = UserMessage.objects.filter(id=int(read_id))
    if msg:
        msg[0].message_status = True
        msg[0].save()
        return JsonResponse({'status': 'ok', 'msg': 'success'})
    else:
        return JsonResponse({'status': 'fail', 'msg': 'fail'})


def user_change_pwd(request):
    user_change_pwd_form = UserPwdForm(request.POST)
    if user_change_pwd_form.is_valid():
        pwd = user_change_pwd_form.cleaned_data['pwd']
        repwd = user_change_pwd_form.cleaned_data['repwd']
        if pwd == repwd:
            user = request.user
            user.set_password(pwd)
            user.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '密码不一致'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '密码不合法'})


def page_error(request):
    return render(request, '500.html')