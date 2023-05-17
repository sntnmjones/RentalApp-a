'''
Profile forms
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    '''
    Create a new user
    '''
    email = forms.EmailField(required=True)

    class Meta:
        '''
        Customize the required fields inherited from UserCreationForm
        '''
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs) -> None:
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

    def save(self, commit=True) -> User:
        '''
        Overrides the inherited save method to use the NewUserForm
        '''
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self) -> str:
        '''
        Check if the email address currently exists. Called by is_valid()
        This prevents more than one user per email
        '''
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already a user registered to this email address")

        return email

class ResetPasswordForm(PasswordResetForm):
    '''
    Password reset form
    '''
    email = forms.EmailField(required=True)

    class Meta:
        '''
        Customize the required fields inherited from PasswordResetForm
        '''
        model = User
        fields = ["username", "email"]


    def clean_email(self) -> str:
        '''
        Check if the email address currently exists. 
        '''
        email = self.cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already a user registered to this email address")

        return email
    