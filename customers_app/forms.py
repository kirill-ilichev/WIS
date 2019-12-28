from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

from customers_app.models import Customer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class UserCustomerForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['age', 'date_of_birth', 'photo']
        widgets = {
            'date_of_birth': AdminDateWidget()
        }
