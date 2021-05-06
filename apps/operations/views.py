from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from courses.models import CourseInfo
from orgs.models import OrgInfo, TeacherInfo
from .models import UserLove, UserComment
from .forms import UserAskForm, UserCommentForm
from utils.decorators import login_decorator
# Create your views here.


def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        user_ask_form.save(commit=True)
        return JsonResponse({'status': 'ok', 'msg': '咨询成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '咨询失败'})

@login_decorator
def user_love(request):
    love_id = request.GET.get('loveid', '')
    love_type = request.GET.get('lovetype', '')
    if all((love_id, love_type)):
        obj = None
        if int(love_type) == 1:
            obj = OrgInfo.objects.filter(id=int(love_id)).first()
        if int(love_type) == 2:
            obj = CourseInfo.objects.filter(id=int(love_id)).first()
        if int(love_type) == 3:
            obj = TeacherInfo.objects.filter(id=int(love_id)).first()

        love = UserLove.objects.filter(love_id=int(love_id), love_type=int(love_type), love_man=request.user)
        if love:
            # 存在收藏记录
            # msg为点击后页面展示的按钮状态
            if love[0].love_status:
                love[0].love_status = False

                obj.love_num -= 1
                obj.save()
                love[0].save()
                return JsonResponse({'status': 'ok', 'msg': '收藏'})
            else:
                love[0].love_status = True
                obj.love_num += 1
                obj.save()
                love[0].save()
                return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
        else:
            # 不存在收藏记录，创建收藏对象，存入数据库
            a = UserLove()
            a.love_man = request.user
            a.love_id = int(love_id)
            a.love_type = int(love_type)
            a.love_status = True
            a.save()
            obj.love_num += 1

            obj.save()
            return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '收藏失败'})


def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        course = user_comment_form.cleaned_data['comment_course']
        content = user_comment_form.cleaned_data['comment_content']
        a = UserComment()
        a.comment_man = request.user
        a.comment_course_id = course
        a.comment_content = content
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '评论成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '评论失败'})


def user_delete_love(request):
    love_id = request.GET.get('love_id')
    love_type = request.GET.get('love_type')
    if all((love_id, love_type)):
        rest = UserLove.objects.filter(love_id=int(love_id),
                                       love_type=int(love_type),
                                       love_man=request.user,
                                       love_status=True)
        if rest:
            rest[0].love_status = False
            rest[0].save()
            return JsonResponse({'status': 'ok', 'msg': '取消成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '取消失败'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '取消失败'})