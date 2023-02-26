from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(
        request,
        template_name="home_page/templates/home_page/index.html",
        context={},
        status=200,
    )
