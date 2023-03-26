import logging
from django.shortcuts import render
from django.shortcuts import render, redirect
from main.forms.profile.forms import NewUserForm, EmailAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

logger = logging.getLogger()
user_profile_template: str = "main/templates/profile/user_profile.html"
login_form_template: str = "main/templates/profile/login_form.html"
new_user_form_template: str = "main/templates/profile/new_user_form.html"

def register(request):
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
            template_name=new_user_form_template,
            context={"errors": form.errors, "register_form": form},
        )
    form = NewUserForm()
    return render(
        request,
        template_name=new_user_form_template,
        context={"register_form": form},
    )


def user_profile(request):
    return render(
        request,
        template_name=user_profile_template,
        context={},
    )


def user_login(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email_address = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=email_address, password=password)
            if user is not None:
                login(request, user)
                return render(
                    request,
                    template_name=user_profile_template,
                    context={"user": user.first_name},
                )
            else:
                return render(
                    request,
                    template_name=login_form_template,
                    context={"login_form": form, "errors": form.errors},
                )
        else:
            return render(
                request,
                template_name=login_form_template,
                context={"login_form": form, "errors": form.errors},
            )
    form = EmailAuthenticationForm()
    return render(
        request=request,
        template_name=login_form_template,
        context={"login_form": form},
    )


def user_logout(request):
    logout(request)
    return redirect("/")
