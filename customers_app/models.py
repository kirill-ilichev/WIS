
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)

    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    age = models.PositiveSmallIntegerField(blank=True)

    date_of_birth = models.DateField(blank=True)
    photo = models.ImageField(blank=True)
    
    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)
