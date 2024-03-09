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
from main.utils.address_utils import get_address_dict
from ...forms.reviews.forms import ReviewForm

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
                _save_review(request.user, form, full_address)
                redirect_url = reverse(
                    "list_reviews",
                    kwargs={
                        "city": city,
                        "state": state,
                        "street": street,
                        "country": country
                    },
                )
                return redirect(redirect_url)
        else:
            if _user_reviewed_address(full_address, request.user):
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
    address_pk = get_address(full_address)
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


def list_reviews_by_city(request, city, state, country):
    """
    /review/list/<country>/<state>/<city>
    List reviews
    """
    reviews = get_city_reviews(city, state, country)
    errors = []
    if 'errors' in request.session:
        errors.append(request.session['errors'])
        request.session.pop('errors', None)

    return render(
        request,
        template_name=common.CITY_REVIEWS_TEMPLATE,
        context={
            "country": country,
            "state": state,
            "city": city,
            "reviews": reviews,
            "errors": errors
        },
    )


def edit_review(request):
    full_address = request.POST.get('address')
    username = request.user.username
    logger.info("username: %s updating: %s", request.user.username, full_address)
    cur_review = get_user_review(username, full_address)
    if request.POST.get('edit') == 'true':
        form = ReviewForm(instance=cur_review)
    else:
        form = ReviewForm(request.POST, instance=cur_review)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    return render(request, common.UPDATE_REVIEW_FORM, {'form': form, 'address': full_address})


def delete_review(request):
    full_address = request.POST.get('address')
    username = request.user.username
    logger.info("username: %s updating: %s", request.user.username, full_address)
    cur_review = get_user_review(username, full_address)
    if request.POST.get('delete') == 'true':
        logger.info(f"username: {username}, deleting review: {cur_review}")
        delete_user_review(cur_review)

    return redirect('user_profile')


def _save_review(user, form: ReviewForm, full_address: str):
    address_pk = get_address(full_address)
    address_dict = get_address_dict(full_address)
    if address_pk is None:
        country = address_dict["country"]
        state = address_dict["state"]
        city = address_dict["city"]
        country_pk = save_country(country)
        state_pk = save_state(country_pk, state)
        city_pk = save_city(state_pk, city)
        address_pk = Address.objects.create(
            full_address=full_address,
            city=city_pk
        )
    review = form.save(commit=False)
    review.address = address_pk
    review.user = user
    with transaction.atomic():
        try:
            review.save()
            logger.info("Review created: %s" % review)
        except Exception as e:
            logger.error("Could not commit transaction: %s" % e)
            transaction.rollback()


def _user_reviewed_address(full_address, user) -> bool:
    if address_pk_exists(full_address):
        address_pk = get_address(full_address)
        reviews = get_reviews(address_pk)
        for review in reviews:
            if review.user == user:
                return True

    return False