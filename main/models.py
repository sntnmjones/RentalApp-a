from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


###############################################################################
# MODELS
###############################################################################
class Address(models.Model):
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.zip_code}"


class Property(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}"

class Review(models.Model):
    RATING_CHOICES = [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=100)
    comment = models.CharField(max_length=3000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    starting_rent = models.IntegerField(
        blank=True, null=True, validators=[MaxValueValidator(999999)]
    )
    starting_rent_month_year = models.DateField(blank=True, null=True)
    ending_rent = models.IntegerField(
        blank=True, null=True, validators=[MaxValueValidator(999999)]
    )
    ending_rent_month_year = models.DateField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    rented_duration_in_months = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(9999)])

    class Meta:
        unique_together = (
            "property",
            "user",
            "starting_rent_month_year",
            "ending_rent_month_year",
        )

    def __str__(self):
        return (
            f"user: {self.user} - rating: {self.rating}"
            f"{self.comment}"
        )
    