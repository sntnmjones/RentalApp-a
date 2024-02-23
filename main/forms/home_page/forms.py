from django import forms
from main.utils.address_utils import get_address_regex_validator

class GetAddressForm(forms.Form):
    address = forms.CharField(
        max_length=100,
        )
