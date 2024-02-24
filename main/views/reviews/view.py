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
from main.utils.common_utils import *
from ...forms.reviews.forms import ReviewForm
from main.utils.address_utils import get_address_dict

logger = logging.getLogger()


def create_review(request, street, city, state, country) -> HttpResponse:
    """
    /review/create/<country>/<state>/<city>/<street>
    Create a new review
    """
    if request.user.is_authenticated:
        full_address = request.session['address']
        address_dict = get_address_dict(full_address)

        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                address_pk = get_address_pk(full_address)
                if address_pk is None:
                    address_pk = Address.objects.create(
                        street=street,
                        city=city,
                        state=state,
                        full_address=full_address
                    )
                    
                review = form.save(commit=False)
                review.address = address_pk
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
                        "country": address_dict["country"]
                    },
                )
                return redirect(redirect_url)
        else:
            if user_reviewed_address(full_address, request.user):
                add_error_to_session_cookie('User has already reviewed address', request)
                redirect_url = reverse(
                    "list_reviews",
                    kwargs={
                        "city": city,
                        "state": state,
                        "street": street,
                        "country": address_dict["country"]
                    },
                )
                return redirect(redirect_url)
            form = ReviewForm()
            return render(request, common.CREATE_REVIEW_FORM, {"form": form})
            

    current_url = request.build_absolute_uri()
    request.session["relay_state_url"] = current_url
    return redirect("user_login")


def list_reviews(request, street, city, state, country):
    """
    /review/list/<country>/<state>/<city>/<street>
    List reviews
    """
    full_address = request.session['address']
    address_dict = get_address_dict(full_address)
    address_pk = get_address_pk(full_address)
    reviews = get_reviews(address_pk=address_pk)
    rating_average = get_rating_average(reviews)
    errors = []
    if 'errors' in request.session:
        errors.append(request.session['errors'])
        request.session.pop('errors', None)

    return render(
        request,
        template_name=common.REVIEW_TEMPLATE,
        context={
            "address": full_address,
            "country": country,
            "state": state,
            "city": city,
            "street": street,
            "reviews": reviews,
            "rating_average": rating_average,
            "errors": errors
        },
    )
