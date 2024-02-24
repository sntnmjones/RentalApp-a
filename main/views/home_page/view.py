"""
Home page view
"""
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from common import INDEX_TEMPLATE, REVIEW_TEMPLATE
from main.utils.database_utils import *
from main.utils.address_utils import get_address_dict
from main.forms.home_page.forms import GetAddressForm


logger = logging.getLogger()


def index(request):
    if request.method == "POST":
        if request.POST.get("address"):
            form = GetAddressForm(request.POST)
            if form.errors:
                logger.error(
                    "Error creating GetaddressAddressForm form: %s",
                    form.errors.as_text,
                )
                return render(
                    request,
                    template_name=INDEX_TEMPLATE,
                    context={"errors": form.errors, "get_address_form": form},
                )
            if form.is_valid():
                full_address = form.cleaned_data["address"]
                request.session['address'] = full_address

                address_dict = get_address_dict(full_address)

                if address_pk_exists(full_address):
                    redirect_url = reverse(
                        "list_reviews",
                        kwargs={
                            "street": address_dict["street"],
                            "city": address_dict["city"],
                            "state": address_dict["state"],
                            "country": address_dict["country"]
                        },
                    )
                    request.session["address"] = full_address
                    return redirect(redirect_url)
                else:
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
                        },
                    )
    else:
        get_address_form = GetAddressForm()
        return render(
            request,
            template_name=INDEX_TEMPLATE,
            context={
                "show_address": False,
                "get_address_form": get_address_form,
            },
        )
