import xadmin
from orgs.models import CityInfo, OrgInfo, TeacherInfo


class CityInfoXadmin(object):
    list_display = ['name', 'add_time']
    model_icon = 'fa fa-university'


class OrgInfoXadmin(object):
    list_display = ['image', 'name', 'course_num', 'study_num', 'love_num', 'click_num', 'category', 'city_info']
    model_icon = 'fa fa-building'
    style_fields = {'detail': 'ueditor'}

class TeacherInfoXadmin(object):
    list_display = ['image', 'name', 'work_year', 'work_position', 'work_style', 'work_company', 'age', 'gender', 'love_num', 'click_num']
    model_icon = 'fa fa-address-card-o'


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)

