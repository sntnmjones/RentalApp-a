"""
Profile views
"""
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from main.forms.profile.forms import NewUserForm

logger = logging.getLogger()

NEW_USER_FORM_TEMPLATE = "main/templates/profile/new_user_form.html"
USER_PROFILE_TEMPLATE = "main/templates/profile/user_profile.html"
LOGIN_FORM_TEMPLATE = "main/templates/profile/login_form.html"


def register(request) -> HttpResponse:
    """
    Register a new user
    """
    logger.info(request.META)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/profile")
        logger.warning("Could not register user. %s", form.errors.as_json)
        return render(
            request,
            template_name=NEW_USER_FORM_TEMPLATE,
            context={"errors": form.errors, "register_form": form},
        )
    form = NewUserForm()
    return render(
        request,
        template_name=NEW_USER_FORM_TEMPLATE,
        context={"register_form": form},
    )


def user_profile(request, context):
    """
    Render user profile template
    """
    return render(
        request,
        template_name=USER_PROFILE_TEMPLATE,
        context=context,
    )


def user_login(request):
    '''
    Show the user login template.
    Log the user in and redirect to the user profile page
    '''
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return user_profile(request, {"username": user.get_username})
            else:
                return render(
                    request,
                    template_name=LOGIN_FORM_TEMPLATE,
                    context={"login_form": form, "errors": form.errors},
                )
        else:
            return render(
                request,
                template_name=LOGIN_FORM_TEMPLATE,
                context={"login_form": form, "errors": form.errors},
            )
    form = AuthenticationForm()
    return render(
        request=request,
        template_name=LOGIN_FORM_TEMPLATE,
        context={"login_form": form},
    )


def user_logout(request):
    '''
    Log the user out and redirect back to home page
    '''
    logout(request)
    return redirect("/")
