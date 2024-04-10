from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("about_us/", about_us, name="about"),
    path("main/", HomePage.as_view(), name='main'),
    path("chats/", ChatsView.as_view(), name="chats"),
    path("chats/<int:id>/", DialogView.as_view(), name="dialog"),
    path('news/', NewslineView.as_view(), name="newsline"),
    path('logout/', logout_user, name="logout"),
    path('get_user/', getting_user),
]


urlpatterns += format_suffix_patterns([
    path('map_info/', get_reviews)
])

print(urlpatterns[-1])