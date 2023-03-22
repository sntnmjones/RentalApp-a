from django import forms

class GetPropertyAddressForm(forms.Form):
    property_address = forms.CharField(label='get_property', max_length=100)