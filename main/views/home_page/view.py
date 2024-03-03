"""
Home page view
"""
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from common import INDEX_TEMPLATE
from main.utils.database_utils import *
from main.utils.address_utils import get_address_dict
from main.forms.home_page.forms import GetAddressForm
from django.http import JsonResponse



logger = logging.getLogger()


def index(request):
    if request.method == "POST":
        if request.POST.get("address"):
            form = GetAddressForm(request.POST)
            if form.errors:
                return _get_index_error_form(request, form)
            if form.is_valid():
                full_address = form.cleaned_data["address"]
                request.session['address'] = full_address
                address_dict = get_address_dict(full_address)

                if address_pk_exists(full_address):
                    return _list_reviews(address_dict)
                else:
                    return _address_not_found(request, full_address, address_dict, form)
    else:
        countries = get_countries()
        return _get_get_address_form(request, countries)


def get_states_list(request):
    """
    Get a list of states for a given country
    """
    states = get_states(request.GET.get('country'))
    return _get_json_response(list(states))


def get_cities_list(request):
    """
    Get a list of cities for a given state
    """
    cities = get_cities(request.GET.get('state'))
    return _get_json_response(list(cities))


def _get_json_response(data: list) -> JsonResponse:
    return JsonResponse(data, safe=False)


def _get_index_error_form(request, form: GetAddressForm):
    logger.error(
        "Error creating GetaddressAddressForm form: %s",
        form.errors.as_text,
    )
    return render(
        request,
        template_name=INDEX_TEMPLATE,
        context={"errors": form.errors, "get_address_form": form},
    )


def _list_reviews(address_dict: dict):
    redirect_url = reverse(
        "list_reviews",
        kwargs={
            "street": address_dict["street"],
            "city": address_dict["city"],
            "state": address_dict["state"],
            "country": address_dict["country"]
        },
    )
    return redirect(redirect_url)


def _address_not_found(request, full_address: str, address_dict: dict, form: GetAddressForm):
    logger.info("Address not found: [%s]", full_address)
    return render(
        request,
        template_name=INDEX_TEMPLATE,
        context={
            "address": full_address,
            "street": address_dict["street"],
            "city": address_dict["city"],
            "state": address_dict["state"],
            "country": address_dict["country"],
            "address_found": False,
            "show_address": True,
            "get_address_form": form,
        }
    )


def _get_get_address_form(request, countries):
    get_address_form = GetAddressForm()
    return render(
        request,
        template_name=INDEX_TEMPLATE,
        context={
            "show_address": False,
            "get_address_form": get_address_form,
            "countries": countries
        },
    )
