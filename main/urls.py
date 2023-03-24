from django.urls import path
from main.views.home_page import view as home_page

urlpatterns = [
    path("", home_page.index, name="index"),
]