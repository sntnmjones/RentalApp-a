from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import logging

logger = logging.getLogger()

def property_not_found(request):
    return render(
        request,
        template_name="property/templates/property_not_found.html",
        context={},
        status=200,
    )