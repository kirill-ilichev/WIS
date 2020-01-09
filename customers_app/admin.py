from django import forms
from django.contrib import admin

from customers_app.models import Customer, Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photo', )


class PhotoAdmin(admin.ModelAdmin):
    form = PhotoForm


admin.site.register(Customer)
admin.site.register(Photo, PhotoAdmin)
