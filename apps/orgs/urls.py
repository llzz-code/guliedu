from django.conf.urls import url
from django.urls import path

from orgs.views import org_list, org_detail, org_detail_course, org_detail_desc, org_detail_teachers, teacher_list,\
    teacher_detail

urlpatterns = [
    path('org_list/', org_list, name='org_list'),
    url(r'^org_detail/(\d+)/$', org_detail, name='org_detail'),
    url(r'^org_detail_course/(\d+)/$', org_detail_course, name='org_detail_course'),
    url(r'^org_detail_desc/(\d+)/$', org_detail_desc, name='org_detail_desc'),
    url(r'^org_detail_teachers/(\d+)/$', org_detail_teachers, name='org_detail_teachers'),
    url(r'^teacher_detail/(\d+)/$', teacher_detail, name='teacher_detail'),
    path('teacher_list/', teacher_list, name='teacher_list')
]
