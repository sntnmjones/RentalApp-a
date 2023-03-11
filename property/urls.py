from django.urls import path
from property import views

urlpatterns = [
    path("404", views.property_not_found, name="property_not_found"),
]