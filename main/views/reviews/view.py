"""
Reviews views
"""
import logging
import common
from main.utils.address_utils import split_street
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from main.models import Address, Property
from ...forms.reviews.forms import ReviewForm

logger = logging.getLogger()

def create_review(request, state, city, street) -> HttpResponse:
    """
    /review/create/<state>/<city>/<street>
    Create a new review
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                street_number, street_name = split_street(street)
                address = Address.objects.create(
                    street_number=street_number,
                    street_name=street_name,
                    city=city,
                    state=state
                )
                review = form.save(commit=False)
                review.property = Property.objects.create(address=address)
                review.user = request.user
                with transaction.atomic():
                    try:
                        review.save()
                        logger.info("Review created: %s" % review)
                    except Exception as e:
                        logger.error("Could not commit transaction: %s" % e)
                        transaction.rollback()
                return redirect('index')
        else:
            form = ReviewForm()
        return render(request, common.CREATE_REVIEW_FORM, {'form': form})

    current_url = request.build_absolute_uri()
    request.session['relay_state_url'] = current_url
    return redirect('user_login')
