from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from courses.models import CourseInfo
from operations.models import UserLove, UserCourse
from django.contrib.auth.decorators import login_required
from utils.decorators import login_decorator

def course_list(request):
    sort = request.GET.get('sort', '')

    all_courses = CourseInfo.objects.all()
    recommend_courses = all_courses.order_by('-add_time')[:3]
    # 全局搜索
    keyword = request.GET.get('keyword', '')
    if keyword:
        all_courses = all_courses.filter(Q(name__icontains=keyword)
                                         | Q(desc__icontains=keyword)
                                         | Q(detail__icontains=keyword))

    if sort:
        all_courses = all_courses.order_by('-' + sort)
    page = request.GET.get('page', 1)
    pages = Paginator(all_courses, 6)
    try:
        pager = pages.page(page)
    except:
        pager = pages.page(1)

    return render(request, 'courses/course-list.html', locals())


def course_detail(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        course.click_num += 1
        course.save()
        related_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[:2]
        love_course = False
        love_org = False
        if request.user.is_authenticated:
            lovecourse = UserLove.objects.filter(love_id=int(course_id),
                                                 love_type=2,
                                                 love_status=True,
                                                 love_man=request.user)
            if lovecourse:
                love_course = True
            loveorg = UserLove.objects.filter(love_id=course.org_info.id, love_type=1,
                                              love_status=True,
                                              love_man=request.user)
            if loveorg:
                love_org = True
        return render(request, 'courses/course-detail.html', locals())


def course_study_list(course_id):
    course = CourseInfo.objects.filter(id=int(course_id)).first()
    # 学过该课的同学还学过
    users = UserCourse.objects.filter(study_course=course).all()
    user_list = [user.study_man for user in users]
    user_course_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course).all()
    courses_list = list(set([user.study_course for user in user_course_list]))[:3]
    return courses_list

@login_decorator
def course_video(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id)).first()

        user_course = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not user_course:
            a = UserCourse()
            a.study_man = request.user
            a.study_course = course
            a.save()
            course.study_num += 1
            course.save()
            # 用户所学的课程
            user_course_list = UserCourse.objects.filter(study_man=request.user).all()
            user_course = [user_course.study_course for user_course in user_course_list]
            # 找出这些课程所对应的机构
            org_list = list(set([course.org_info for course in user_course]))
            # 如果新学习的课程机构不在学生所学习过的机构列表中，则该机构的学习人数+1
            if course.org_info not in org_list:
                course.org_info.study_num += 1
                course.org_info.save()

        # 学过该课的同学还学过
        courses_list = course_study_list(course_id)

        return render(request, 'courses/course-video.html', locals())


def course_comment(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id)).first()
        comment_list = course.usercomment_set.all()
        courses_list = course_study_list(course_id)
        return render(request, 'courses/course-comment.html', locals())
