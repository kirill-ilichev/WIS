from django import forms
from django.contrib import admin

from customers_app.models import Customer, Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photo', )


class PhotoAdmin(admin.ModelAdmin):
    form = PhotoForm


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'age', 'date_of_birth']

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for customer in queryset:
            customer.delete()

        queryset.delete()


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Photo, PhotoAdmin)
