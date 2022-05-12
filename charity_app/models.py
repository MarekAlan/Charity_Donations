from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


TYPES = (
    ("Fundacja", "Fundacja"),
    ("Organizacja Pozarządowa", "Organizacja Pozarządowa"),
    ("Zbiórka Lokalna", "Zbiórka Lokalna"),
)


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(max_length=64, choices=TYPES, default="Fundacja")
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


