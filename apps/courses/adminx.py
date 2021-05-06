
import xadmin
from courses.models import SourceInfo, VideoInfo, LessonInfo, CourseInfo
from xadmin import views

# 配置xadmin主题
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalXadminSetting(object):
    site_title = '谷粒教育后台管理系统'
    site_footer = '尚硅谷it教育'
    menu_style = 'accordion'


class CourseInfoXadmin(object):
    list_display = ['image', 'name', 'study_time', 'study_num', 'level', 'love_num', 'click_num',
                    'desc', 'category', 'org_info', 'teacher_Info']
    model_icon = 'fa fa-folder-o'
    style_fields = {'detail': 'ueditor'}


class LessonInfoXadmin(object):
    list_display = ['name', 'course_info']
    model_icon = 'fa fa-folder-open-o'


class VideoInfoXadmin(object):
    list_display = ['name', 'study_time', 'url']
    model_icon = 'fa fa-film'


class SourceInfoXadmin(object):
    list_display = ['name', 'download']
    model_icon = 'fa fa-database'


xadmin.site.register(SourceInfo, SourceInfoXadmin)
xadmin.site.register(VideoInfo, VideoInfoXadmin)
xadmin.site.register(LessonInfo, LessonInfoXadmin)
xadmin.site.register(CourseInfo, CourseInfoXadmin)
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)
xadmin.site.register(views.CommAdminView, GlobalXadminSetting)
