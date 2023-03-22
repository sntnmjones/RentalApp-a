from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.zip_code}"

class Property(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    reviews = models.ManyToManyField('Review')

    def __str__(self):
        return f"{self.address}"

class Review(models.Model):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    reviewed_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    starting_rent = models.IntegerField(max_length=5, default=0)
    ending_rent = models.IntegerField(max_length=5, default=0)
    comment = models.CharField(max_length=3000)

    def __str__(self):
        return f"{self.user} - {self.rating} - {self.comment}"
