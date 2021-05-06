from django.urls import path
from .views import user_ask, user_love, user_comment, user_delete_love


urlpatterns = [
    path('user_ask/', user_ask, name='user_ask'),
    path('user_love/', user_love, name='user_love'),
    path('user_comment/', user_comment, name='user_comment'),
    path('user_delete_love/', user_delete_love, name='user_delete_love'),
]
