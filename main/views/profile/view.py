import logging
from django.shortcuts import render
from django.shortcuts import render, redirect
from main.forms.profile.forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

logger = logging.getLogger()


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
            template_name="main/templates/profile/new_user_form.html",
            context={"errors": form.errors, "register_form": form},
        )
    form = NewUserForm()
    return render(
        request,
        template_name="main/templates/profile/new_user_form.html",
        context={"register_form": form},
    )


def user_profile(request):
    return render(
        request,
        template_name="main/templates/profile/user_profile.html",
        context={},
    )


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return user_profile(request)
            else:
                return render(
                    request,
                    template_name="main/templates/profile/login_form.html",
                    context={"login_form": form, "errors": form.errors},
                )
        else:
            return render(
                request,
                template_name="main/templates/profile/login_form.html",
                context={"login_form": form, "errors": form.errors},
            )
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="main/templates/profile/login_form.html",
        context={"login_form": form},
    )

def user_logout(request):
	logout(request)
	return redirect("/")