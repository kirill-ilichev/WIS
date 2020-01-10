from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from customers_app.models import Customer, Photo


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(max_length=30)
        self.fields['last_name'] = forms.CharField(max_length=150)


UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'password1', 'password2', 'first_name', 'last_name')
    }),
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ('points', )
    list_display = ['__str__', 'points']


admin.site.register(Photo, PhotoAdmin)


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('age', )
    list_display = ['__str__', 'user', 'age', 'date_of_birth', 'id']

    def delete_queryset(self, request, queryset):
        """
        Overwrite delete_queryset() method
        to use Customer's delete() method
        """
        for customer in queryset:
            customer.delete()

        queryset.delete()


admin.site.register(Customer, CustomerAdmin)
