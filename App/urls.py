from django.urls import path

from .views import *

urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("about_us/", about_us, name="about"),
    path("main/", HomePage.as_view(), name='main'),
    path('logout/', logout_user, name="logout")
]
