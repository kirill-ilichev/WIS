from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    photo = models.ImageField(blank=True, null=True)
    points = models.PositiveSmallIntegerField(blank=True, default=0)

    def add_point_to_photo(self):
        Photo.objects.select_for_update(). \
            filter(pk=self.pk). \
            update(points=models.F('points') + 1)

    max_points = 10


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.PositiveSmallIntegerField(blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} customer".format(self.pk)
