from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("", views.Login.as_view(), name="login"),
    path("about_us/", views.about_us, name="about"),
    path("main/", views.HomePage.as_view(), name='main'),
    path("chats/", views.ChatsView.as_view(), name="chats"),
    path("profile/<int:user_id>/", views.ProfilePageView.as_view(), name="profile"),
    path("chats/<int:id>/", views.DialogView.as_view(), name="dialog"),
    path('news/', views.NewslineView.as_view(), name="newsline"),
    path('logout/', views.logout_user, name="logout"),
    path('get_user/', views.getting_user),
]