"""
Models
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


###############################################################################
# MODELS
###############################################################################
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    full_address = models.CharField(max_length=300)

    def __str__(self):
        return f"Address: {self.street}, {self.city}, {self.state}"


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

    class Meta:
        unique_together = (
            "property",
            "user",
            "starting_rent_month_year",
            "ending_rent_month_year",
        )

    def __str__(self):
        return (
            f"property: {self.property}"
            f" - user: {self.user}"
        )
    