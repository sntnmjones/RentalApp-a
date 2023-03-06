from django.shortcuts import render
import logging

logger = logging.getLogger()

def index(request):
    return render(
        request,
        template_name="home_page/templates/home_page/index.html",
        context={},
        status=200,
    )
