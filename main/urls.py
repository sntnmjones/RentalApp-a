from django.urls import path
from main.views.home_page import view as home_page
from main.views.profile import view as profile
from main.views.reviews import view as reviews


urlpatterns = [
    path("", home_page.index, name="index"),
    path("register", profile.register, name="register"),
    path("login", profile.user_login, name="user_login"),
    path("logout", profile.user_logout, name="user_logout"),
    path("profile", profile.user_profile, name="user_profile"),
    path("username", profile.forgot_username, name="forgot_username"),
    path("password", profile.CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/confirm/<uidb64>/<token>/",
        profile.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("review/create/<state>/<city>/<street>", reviews.create_review, name="create_review")
]
