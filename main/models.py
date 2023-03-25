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
    property_review = models.ManyToManyField('Review')
    rating = models.FloatField()

    def __str__(self):
        return f"{self.address} - {self.rating}"

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
    starting_rent = models.IntegerField(default=0)
    ending_rent = models.IntegerField(default=0)
    comment = models.CharField(max_length=3000)
    pub_date = models.DateTimeField('date published')
    rented_duration = models.IntegerField()

    def __str__(self):
        return (f"user: {self.user} - rating: {self.rating} - rented_duration: {self.rented_duration}"
        f"{self.comment}")
