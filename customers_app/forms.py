from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

from customers_app.models import Customer


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def is_passwords_match(self):
        print(self)

        cleaned_data = self.cleaned_datas
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            msg = 'Passwords doen\'t match'
            self.errors['password'] = self.error_class([msg])

            del cleaned_data['password']
            del cleaned_data['confirm_password']
            return False
        return True

    def is_user_exist(self):
        print(self)

        cleaned_data = self.cleaned_data
        try:
            User.objects.get(username=cleaned_data['username'])
            return True
        except User.DoesNotExist:
            self.errors['username'] = self.error_class(['There is no User with this username'])
            del cleaned_data['username']
            return False

    def is_password_correct(self):
        print(self)

        cleaned_data = self.cleaned_data
        if self.user_exist() and \
                not User.objects.get(username=cleaned_data['username']).check_password(cleaned_data['password']):
            self.errors['password'] = self.error_class(['Wrong password'])
            del cleaned_data['password']
            return False
        return True


class UserCustomerForm(UserForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta(UserForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class CustomerForm(forms.ModelForm):

    class Meta():
        model = Customer
        fields = ['age', 'date_of_birth', 'photo']
        widgets = {
            'date_of_birth': AdminDateWidget()
        }
