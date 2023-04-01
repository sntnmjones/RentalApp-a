"""
Reviews views
"""
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ...forms.reviews.forms import ReviewForm

logger = logging.getLogger()

CREATE_REVIEW_FORM = "main/templates/reviews/create_review_form.html"


def create_review(request, state, city, street) -> HttpResponse:
    """
    /review/create/<state>/<city>/<street>
    Create a new review
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                # review.user = request.user
                # review.save()
                return redirect('index')
        else:
            form = ReviewForm()
        return render(request, CREATE_REVIEW_FORM, {'form': form})

    current_url = request.build_absolute_uri()
    request.session['relay_state_url'] = current_url
    return redirect('user_login')
