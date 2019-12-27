from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from customers_app.models import Customer
from customers_app.forms import UserForm, CustomerForm,  UserCustomerForm


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
            if user_form.is_passwords_match():
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
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        if user_form.is_user_exist():
            if user_form.is_passwords_match():
                if user_form.is_password_correct():
                    pass

        return render(request, self.template_name, {'form': user_form})
