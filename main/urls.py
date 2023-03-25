from django.urls import path
from main.views.home_page import view as home_page
from main.views.profile import view as profile

urlpatterns = [
    path("", home_page.index, name="index"),
    path("register", profile.register, name="register"),
    path("login", profile.user_login, name="user_login"),
    path("logout", profile.user_logout, name="user_logout"),
    path("profile", profile.user_profile, name="user_profile")
]