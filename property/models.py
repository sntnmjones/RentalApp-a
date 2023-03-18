from django.db import models

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
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.reviewer_name} - {self.rating} - {self.comment}"
