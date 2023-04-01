import logging
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render

from main.forms.home_page.forms import GetPropertyAddressForm


logger = logging.getLogger()
index_template: str = "main/templates/home_page/index.html"


def index(request):
    if request.method == "POST":
        if request.POST.get("property_address"):
            return _get_property_address(request)
    else:
        get_property_address_form = GetPropertyAddressForm()
        return render(
            request,
            template_name=index_template,
            context={
                "show_property_address": False,
                "get_property_address_form": get_property_address_form,
            },
        )


def _get_property_address(request):
    form = GetPropertyAddressForm(request.POST)
    if form.errors:
        logger.error(
            "Error creating GetPropertyAddressForm form: %s", form.errors.as_text
        )
        return render(
            request,
            template_name=index_template,
            context={"errors": form.errors, "get_property_address_form": form},
        )
    if form.is_valid():
        address = form.cleaned_data["property_address"]
        logger.info("Getting Address: [%s]", address)

        # TODO: Find the address
        property_found = False

        if property_found:
            # TODO: Go to property url
            pass
        else:
            logger.info("Address not found: [%s]", address)
            fields = address.split(', ')
            fields = [f.replace(' ', '-').lower() for f in fields]
            street = fields[0]
            city = fields[1]
            state = fields[2]
            return render(
                request,
                template_name=index_template,
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
