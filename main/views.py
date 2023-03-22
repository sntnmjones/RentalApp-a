import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render

from main.forms import GetPropertyAddressForm

logger = logging.getLogger()

def index(request):
    logger.info(f"Hey from property_address")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GetPropertyAddressForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = NameForm()

    return render(
        request,
        template_name="main/templates/home_page/index.html",
        context={},
        status=200,
    )
