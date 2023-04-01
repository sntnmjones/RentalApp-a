"""
Reviews views
"""
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

logger = logging.getLogger()

CREATE_REVIEW_FORM = "main/templates/reviews/create_review_form.html"

def create_review(request) -> HttpResponse:
    """
    /review/create
    Create a new review
    """
    return render(request, CREATE_REVIEW_FORM)
