from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import logging

logger = logging.getLogger()

def index(request):
    return render(
        request,
        template_name="main/templates/home_page/index.html",
        context={},
        status=200,
    )
