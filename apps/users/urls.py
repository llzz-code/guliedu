from django.conf.urls import url
from django.urls import path

from users.views import RegisterView, LoginView, user_logout, user_active, ForgetView, user_reset, user_info, \
    user_changeimage, user_changeinfo, user_changeemail, user_resetemail, user_course, user_fav_org, user_fav_teacher,\
    user_fav_course, user_message, user_message_read, user_change_pwd

urlpatterns = [
    path('user_register/', RegisterView.as_view(), name='user_register'),
    path('user_login/', LoginView.as_view(), name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    url(r'^user_active/(.*)/$', user_active, name='user_active'),
    path('user_forget/', ForgetView.as_view(), name='user_forget'),
    url(r'^user_reset/(.*)/$', user_reset, name='user_reset'),
    path('user_info/', user_info, name='user_info'),
    path('user_changeimage/', user_changeimage, name='user_changeimage'),
    path('user_changeinfo/', user_changeinfo, name='user_changeinfo'),
    path('user_changeemail/', user_changeemail, name='user_changeemail'),
    path('user_resetemail/', user_resetemail, name='user_resetemail'),
    path('user_course/', user_course, name='user_course'),
    path('user_fav_org/', user_fav_org, name='user_fav_org'),
    path('user_fav_course/', user_fav_course, name='user_fav_course'),
    path('user_fav_teacher/', user_fav_teacher, name='user_fav_teacher'),
    path('user_message/', user_message, name='user_message'),
    path('user_message_read/', user_message_read, name='user_message_read'),
    path('user_change_pwd/', user_change_pwd, name='user_change_pwd'),

]
