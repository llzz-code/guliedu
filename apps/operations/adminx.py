
import xadmin
# Create your models here.
from operations.models import UserAsk, UserLove, UserCourse, UserComment, UserMessage


class UserAskXadmin(object):
    list_display = ['name', 'phone', 'course']
    model_icon = 'fa fa-envelope-open-o'


class UserLoveXadmin(object):
    list_display = ['love_man', 'love_id', 'love_type', 'love_status']
    model_icon = 'fa fa-cube'


class UserCourseXadmin(object):
    list_display = ['study_man', 'study_course']
    model_icon = 'fa fa-graduation-cap'


class UserCommentXadmin(object):
    list_display = ['comment_man', 'comment_course', 'comment_content']
    model_icon = 'fa fa-language'


class UserMessageXadmin(object):
    list_display = ['message_man', 'message_content', 'message_status']
    model_icon = 'fa fa-commenting-o'


xadmin.site.register(UserMessage, UserMessageXadmin)
xadmin.site.register(UserComment, UserCommentXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserLove, UserLoveXadmin)
xadmin.site.register(UserAsk, UserAskXadmin)


