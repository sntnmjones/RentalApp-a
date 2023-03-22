import logging
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render

from main.forms import GetPropertyAddressForm

logger = logging.getLogger()

def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GetPropertyAddressForm(request.POST)
        if form.errors:
            logger.error("Error creating GetPropertyAddressForm form: %s", form.errors.as_text)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')
            return HttpResponse(form.cleaned_data['property_address'])

    # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = NameForm()

    return render(
        request,
        template_name="main/templates/home_page/index.html",
        context={},
        status=200,
    )
