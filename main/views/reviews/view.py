"""
Reviews views
"""
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import transaction
import common
from main.models import Address
from main.utils.database_utils import *
from main.utils.review_utils import *
from ...forms.reviews.forms import ReviewForm

logger = logging.getLogger()


def create_review(request, street, city, state) -> HttpResponse:
    """
    /review/create/<state>/<city>/<street>
    Create a new review
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                address = get_address_pk(street, city, state)
                if address is None:
                    address = Address.objects.create(
                        street=street,
                        city=city,
                        state=state,
                        full_address=request.session['address']
                    )
                    
                review = form.save(commit=False)
                review.address = address
                review.user = request.user
                with transaction.atomic():
                    try:
                        review.save()
                        logger.info("Review created: %s" % review)
                    except Exception as e:
                        logger.error("Could not commit transaction: %s" % e)
                        transaction.rollback()
                redirect_url = reverse(
                    "list_reviews",
                    kwargs={
                        "city": city,
                        "state": state,
                        "street": street,
                    },
                )
                return redirect(redirect_url)
        else:
            form = ReviewForm()
        return render(request, common.CREATE_REVIEW_FORM, {"form": form})

    current_url = request.build_absolute_uri()
    request.session["relay_state_url"] = current_url
    return redirect("user_login")


def list_reviews(request, street, city, state):
    """
    /review/list/<state>/<city>/<street>
    List reviews
    """
    address_pk = get_address_pk(street, city, state)
    reviews = get_reviews(address_pk=address_pk)
    address = request.session["address"]
    rating_average = get_rating_average(reviews)
    return render(
        request,
        template_name=common.REVIEW_TEMPLATE,
        context={
            "address": address,
            "state": state,
            "city": city,
            "street": street,
            "reviews": reviews,
            "rating_average": rating_average
        },
    )
