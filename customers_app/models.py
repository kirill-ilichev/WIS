from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    photo = models.ImageField()
    points = models.PositiveSmallIntegerField(blank=True, default=0)

    def add_point_to_photo(self):
        Photo.objects.select_for_update(). \
            filter(pk=self.pk). \
            update(points=models.F('points') + 1)

    max_points = 10


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.PositiveSmallIntegerField()

    date_of_birth = models.DateField()

    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{0} customer".format(self.pk)
