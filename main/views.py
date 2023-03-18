import logging
from django.shortcuts import render

logger = logging.getLogger()

def index(request):
    return render(
        request,
        template_name="main/templates/home_page/index.html",
        context={},
        status=200,
    )
