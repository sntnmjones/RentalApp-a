from django import forms

class GetPropertyAddressForm(forms.Form):
    property_address = forms.CharField(max_length=100)