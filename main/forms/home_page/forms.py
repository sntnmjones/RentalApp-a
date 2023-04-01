from django import forms
from main.utils.address_utils import get_address_regex_validator

class GetPropertyAddressForm(forms.Form):
    property_address = forms.CharField(
        max_length=100,
        validators=[get_address_regex_validator()]
        )
