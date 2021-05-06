from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from operations.models import UserLove
from orgs.models import OrgInfo, TeacherInfo, CityInfo

# Create your views here.


def org_list(request):
    city_list = CityInfo.objects.all()
    org_list = OrgInfo.objects.all()
    sort_org = org_list.order_by('-love_num')[:3]

    # 全局搜索
    keyword = request.GET.get('keyword', '')
    if keyword:
        org_list = org_list.filter(Q(name__icontains=keyword)
                                   | Q(desc__icontains=keyword)
                                   | Q(detail__icontains=keyword))
    # 按照机构类别过滤
    cate = request.GET.get('cate', '')
    cityid = request.GET.get('cityid', '')
    sort = request.GET.get('sort', '')
    if cate:
        org_list = org_list.filter(category=cate)
    if cityid:
        org_list = org_list.filter(city_info__id=cityid)
    if sort:
        org_list = org_list.order_by('-'+sort)

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(org_list, 3)
    try:
        pager = paginator.page(page)  # 查询第page页
    except:
        pager = paginator.page(1)
    return render(request, 'orgs/org-list.html', locals())


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=org_id)[0]
        # 点击数加1
        org.click_num += 1
        org.save()
        # 返回用户收藏状态
        love_status = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1)
            if love:
                love_status = True
        detail_type = 'home'
        return render(request, 'orgs/org-detail-homepage.html', locals())


def org_detail_course(request, org_id):
    if org_id:
        detail_type = 'course'
        org = OrgInfo.objects.filter(id=org_id)[0]
        course_list = org.courseinfo_set.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(course_list, 4)
        love_status = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1)
            if love:
                love_status = True
        try:
            pager = paginator.page(page)
        except:
            pager = paginator.page(1)
        return render(request, 'orgs/org-detail-course.html', locals())


def org_detail_desc(request, org_id):
    if org_id:
        detail_type = 'desc'
        love_status = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1)
            if love:
                love_status = True
        org = OrgInfo.objects.filter(id=org_id)[0]
        return render(request, 'orgs/org-detail-desc.html', locals())


def org_detail_teachers(request, org_id):
    if org_id:
        detail_type = 'teacher'
        love_status = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1)
            if love:
                love_status = True
        org = OrgInfo.objects.filter(id=org_id)[0]
        teachers = org.teacherinfo_set.all()
        return render(request, 'orgs/org-detail-teachers.html', locals())


def teacher_list(request):
    all_teachers = TeacherInfo.objects.all()
    sort_teacher = all_teachers.order_by('-love_num')[:5]
    sort = request.GET.get('sort', '')

    # 全局搜索
    keyword = request.GET.get('keyword', '')
    if keyword:
        all_teachers = all_teachers.filter(name__icontains=keyword)
    if sort:
        all_teachers = all_teachers.order_by('-' + sort)
    page = request.GET.get('page', 1)
    pages = Paginator(all_teachers, 3)
    try:
        pager = pages.page(page)
    except:
        pager = pages.page(1)
    return render(request, 'teacher/teachers-list.html', locals())


def teacher_detail(request, teacher_id):
    if teacher_id:
        teacher = TeacherInfo.objects.filter(id=int(teacher_id)).first()
        teacher.click_num += 1
        teacher.save()
        all_teachers = TeacherInfo.objects.all()
        sort_teacher = all_teachers.order_by('-love_num')[:5]
        course_list = teacher.courseinfo_set.all()
        page = request.GET.get('page', 1)
        pages = Paginator(course_list, 3)
        try:
            pager = pages.page(page)
        except:
            pager = pages.page(1)

        love_teacher = False
        love_org = False
        if request.user.is_authenticated:
            loveteacher = UserLove.objects.filter(love_id=int(teacher_id),
                                                  love_type=3,
                                                  love_status=True,
                                                  love_man=request.user)
            if loveteacher:
                love_teacher = True
            loveorg = UserLove.objects.filter(love_id=teacher.work_company.id, love_type=1,
                                              love_status=True,
                                              love_man=request.user)
            if loveorg:
                love_org = True
        return render(request, 'teacher/teacher-detail.html', locals())
