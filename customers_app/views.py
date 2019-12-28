from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from customers_app.forms import CustomerForm,  UserCustomerForm, LoginForm
from customers_app.helpers import is_passwords_match
from customers_app.models import Customer


class CustomersListView(TemplateView):
    template_name = "customers_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        customers = Customer.objects.all()
        query_filter = self.request.GET.get('filter', None)
        if query_filter:
            customers = customers.order_by('-{}'.format(query_filter))

        context['customers'] = customers
        return context


class CustomersCreateView(View):
    customer_form_class = CustomerForm
    user_form_class = UserCustomerForm
    template_name = 'customers_create.html'

    def get(self, request, *args, **kwargs):
        customer_form = self.customer_form_class
        user_form = self.user_form_class
        return render(request, self.template_name, {'user_form': user_form, 'customer_form': customer_form})

    def post(self, request, *args, **kwargs):
        user_form = UserCustomerForm(request.POST)

        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            if is_passwords_match(user_form):
                user_cleaned_data = user_form.cleaned_data
                user_cleaned_data.pop('confirm_password')

                user = User.objects.create_user(**user_cleaned_data)
                customer = customer_form.save(commit=False)
                customer.user = user
                customer.save()

                return redirect('customers-list')

        return render(request, self.template_name, {'user_form': user_form, 'customer_form': customer_form})


class CustomersAuthView(View):
    template_name = 'customers_auth.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            if is_passwords_match(user_form):
                cd = user_form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user:
                    login(request, user)
                    return redirect('customers-list')
                else:
                    msg = 'Invalid login or password'
                    user_form.errors['username'] = user_form.error_class([msg])

                    del cd['username']

        return render(request, self.template_name, {'form': user_form})
