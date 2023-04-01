"""
Profile views
"""
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from main.forms.profile.forms import NewUserForm
from rental_app.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

logger = logging.getLogger()

NEW_USER_FORM_TEMPLATE = "main/templates/profile/new_user_form.html"
USER_PROFILE_TEMPLATE = "main/templates/profile/user_profile.html"
LOGIN_FORM_TEMPLATE = "main/templates/profile/login_form.html"
FORGOT_USERNAME_FORM_TEMPLATE = "main/templates/profile/forgot_username_form.html"
FORGOT_PASSWORD_FORM_TEMPLATE = "main/templates/profile/forgot_password_form.html"
FORGOT_USERNAME_EMAIL = "main/templates/profile/forgot_username_email.html"
PASSWORD_RESET_EMAIL_FORM_TEMPLATE = (
    "main/templates/profile/password_reset_email_form.html"
)
PASSWORD_RESET_CONFIRM_FORM_TEMPLATE = (
    "main/templates/profile/password_reset_confirm_form.html"
)


def forgot_username(request) -> HttpResponse:
    """
    Forgot username workflow
    Returns the user to the login page
    """
    message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            domain = HttpRequest.get_host(request)
            protocol = 'https' if request.is_secure() else 'http'

            email_html = render_to_string(FORGOT_USERNAME_EMAIL, {
                'username': user.username,
                'domain': domain,
                'protocol': protocol
            })
            send_mail(
                "Rentalranter Username",
                "",
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                auth_user=EMAIL_HOST_USER,
                auth_password=EMAIL_HOST_PASSWORD,
                html_message=email_html
            )
        except User.DoesNotExist:
            pass
        message = "If there is a user with that email address, you'll receive an email shortly"
        return render(request, FORGOT_USERNAME_FORM_TEMPLATE, {"message": message})
    return render(request, FORGOT_USERNAME_FORM_TEMPLATE)


def forgot_password(request) -> HttpResponse:
    """
    /password
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name="password_reset_subject.txt",
                email_template_name="password_reset_email.html",
                html_email_template_name="password_reset_email.html",
                extra_email_context=None,
            )
            return redirect("user_login")
    else:
        form = PasswordResetForm()
    return render(request, FORGOT_PASSWORD_FORM_TEMPLATE, {"form": form})


def register(request) -> HttpResponse:
    """
    /register
    Register a new user
    Forwards the user to the registration page
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


def user_profile(request, context) -> HttpResponse:
    """
    /profile
    Render user profile template
    """
    return render(
        request,
        template_name=USER_PROFILE_TEMPLATE,
        context=context,
    )


def user_login(request) -> HttpResponse:
    """
    /login
    Show the user login template.
    Log the user in and redirect to the user profile page
    """
    if request.method == "POST":
        forgot_username(request)

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.session['relay_state_url']:
                    return redirect(request.session['relay_state_url'])
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


def user_logout(request) -> HttpResponseRedirect:
    """
    /logout
    Log the user out and redirect back to home page
    """
    logout(request)
    return redirect("/")


class CustomPasswordResetView(PasswordResetView):
    email_template_name = PASSWORD_RESET_EMAIL_FORM_TEMPLATE
    success_url = reverse_lazy("user_login")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = PASSWORD_RESET_CONFIRM_FORM_TEMPLATE
    success_url = reverse_lazy("user_login")
