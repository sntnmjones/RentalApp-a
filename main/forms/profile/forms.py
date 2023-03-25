from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a "show password" button next to the password field
        self.fields["password1"].widget.attrs["class"] = "password-field"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields[
            "password1"
        ].help_text = """
        <div class="password-toggle-container">
            <input type="checkbox" onclick="togglePasswordVisibility()">
            <span class="password-toggle-label">Show password</span>
        </div>
        """

    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
