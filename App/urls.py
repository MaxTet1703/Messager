from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('map_info/', get_reviews, basename="MapInfo")

urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("about_us/", about_us, name="about"),
    path("main/", HomePage.as_view(), name='main'),
    path("chats/", ChatsView.as_view(), name="chats"),
    path("chats/<int:id>/", DialogView.as_view(), name="dialog"),
    path('news/', NewslineView.as_view(), name="newline"),
    path('logout/', logout_user, name="logout"),
    path('get_user/', getting_user),
    path("api/", include("rest_framework.urls"))
]

