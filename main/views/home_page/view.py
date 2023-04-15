"""
Home page view
"""
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from common import INDEX_TEMPLATE, REVIEW_TEMPLATE
from main.utils.database_utils import *
from main.utils.address_utils import get_address_dict
from main.forms.home_page.forms import GetPropertyAddressForm


logger = logging.getLogger()


def index(request):
    if request.method == "POST":
        if request.POST.get("property_address"):
            form = GetPropertyAddressForm(request.POST)
            if form.errors:
                logger.error(
                    "Error creating GetPropertyAddressForm form: %s",
                    form.errors.as_text,
                )
                return render(
                    request,
                    template_name=INDEX_TEMPLATE,
                    context={"errors": form.errors, "get_property_address_form": form},
                )
            if form.is_valid():
                address = form.cleaned_data["property_address"]

                address_dict = get_address_dict(address)

                if property_pk_exists(
                    address_dict["street_number"],
                    address_dict["street_name"],
                    address_dict["city"],
                    address_dict["state"],
                ):
                    redirect_url = reverse(
                        "list_reviews",
                        kwargs={
                            "city": address_dict["city"],
                            "state": address_dict["state"],
                            "street": address_dict["street"],
                        },
                    )
                    request.session["address"] = address
                    return redirect(redirect_url)
                else:
                    logger.info("Address not found: [%s]", address)
                    return render(
                        request,
                        template_name=INDEX_TEMPLATE,
                        context={
                            "address": address,
                            "street": street,
                            "city": city,
                            "state": state,
                            "property_found": False,
                            "show_property_address": True,
                            "get_property_address_form": form,
                        },
                    )
    else:
        get_property_address_form = GetPropertyAddressForm()
        return render(
            request,
            template_name=INDEX_TEMPLATE,
            context={
                "show_property_address": False,
                "get_property_address_form": get_property_address_form,
            },
        )
