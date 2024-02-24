from django.urls import path
from main.views.home_page import view as home_page
from main.views.profile import view as profile
from main.views.reviews import view as reviews
from django.contrib.auth import views as auth_views
import common


urlpatterns = [
    path("", home_page.index, name="index"),
    path("register", profile.register, name="register"),
    path("login", profile.user_login, name="user_login"),
    path("logout", profile.user_logout, name="user_logout"),
    path("profile", profile.user_profile, name="user_profile"),
    path("forgot-username", profile.forgot_username, name="forgot_username"),
    path("forgot-password", profile.password_reset, name="password_reset"),
    path(
        "password/confirm/<uidb64>/<token>/",
        profile.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
        ),
    path("review/create/<country>/<state>/<city>/<street>", reviews.create_review, name="create_review"),
    path("review/list/<country>/<state>/<city>/<street>", reviews.list_reviews, name="list_reviews")
]