"""
Home page view
"""
import logging
from common import INDEX_TEMPLATE, REVIEW_TEMPLATE
from main.utils.database_utils import *
from main.utils.address_utils import split_street
from main.forms.home_page.forms import GetPropertyAddressForm
from django.shortcuts import render


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
                logger.info("Getting Address: [%s]", address)

                fields = address.split(", ")
                fields = [f.replace(" ", "-").lower() for f in fields]
                street = fields[0]
                city = fields[1]
                state = fields[2]
                street_number, street_name = split_street(street)

                property_pk = get_property_pk(
                    street_number=street_number,
                    street_name=street_name,
                    city=city,
                    state=state,
                )

                reviews = get_reviews(property_pk=property_pk)

                logger.info(reviews)
                if reviews:
                    return render(
                    request,
                    template_name=REVIEW_TEMPLATE,
                    context={
                        "address": address,
                        "reviews": reviews,
                    },
                )
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
