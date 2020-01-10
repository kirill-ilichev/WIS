from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Photo(models.Model):
    photo = models.ImageField()
    points = models.PositiveSmallIntegerField(blank=True, default=0)

    def add_point(self):
        photo = Photo.objects.select_for_update().filter(pk=self.pk)
        if photo.first().points < self.max_points:
            photo.update(points=models.F('points') + 1)

    max_points = 10

    def __str__(self):
        return "{}".format(self.photo.name)


def validate_date_of_birth(value):
    if value > datetime.now().date():
        raise ValidationError('Date of birth cannot be greater than the current date')


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.PositiveSmallIntegerField(blank=True, null=False)

    date_of_birth = models.DateField(validators=[validate_date_of_birth])

    photo = models.OneToOneField(Photo, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.user.username, self.user.first_name, self.user.last_name)

    def delete(self, *args, **kwargs):
        self.user.delete()
        if self.photo:
            self.photo.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def save(self, **kwargs):
        self.age = relativedelta(datetime.now().date(), self.date_of_birth).years
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
