from django import forms
from django.contrib.auth.models import User

from customers_app.models import Customer


class LoginForm(forms.Form):
    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class UserForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email']


class UserCreateForm(UserForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields + ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput()
        }


class CustomerForm(forms.ModelForm):
    photo = forms.ImageField()

    class Meta:
        model = Customer
        fields = ['date_of_birth']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'DD.MM.YYYY'})
        }
