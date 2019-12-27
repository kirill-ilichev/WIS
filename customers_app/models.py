from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)

    age = models.PositiveSmallIntegerField(blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return "{0} customer".format(self.pk)
