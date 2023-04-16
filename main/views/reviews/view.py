"""
Reviews views
"""
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
import common
from main.models import Address, Property
from main.utils.address_utils import split_street
from main.utils.database_utils import *
from main.utils.address_utils import split_street
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
                address = Address.objects.create(
                    street=street,
                    city=city,
                    state=state,
                    full_address=request.session['address']
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
                return redirect("index")
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
    property_pk = get_property_pk(street, city, state)
    reviews = get_reviews(property_pk=property_pk)
    address = request.session["address"]
    return render(
        request,
        template_name=common.REVIEW_TEMPLATE,
        context={
            "address": address,
            "state": state,
            "city": city,
            "street": street,
            "reviews": reviews,
        },
    )
