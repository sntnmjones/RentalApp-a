from django import forms
from ...models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title',
            'comment',
            'rating',
            'starting_rent',
            'starting_rent_month_year',
            'ending_rent',
            'ending_rent_month_year',
        ]
        widgets = {
            'starting_rent_month_year': forms.DateInput(attrs={'type': 'date'}),
            'ending_rent_month_year': forms.DateInput(attrs={'type': 'date'}),
        }
