from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from customers_app.forms import CustomerForm,  UserCustomerForm, LoginForm
from customers_app.helpers import is_passwords_match, sort_customers
from customers_app.models import Customer


class CustomersListView(TemplateView):
    template_name = "customers_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        customers = Customer.objects.all()

        if self.request.method == 'GET':
            field_for_ordering = self.request.GET.get('filter', None)
            if field_for_ordering:
                sorted_customers = sort_customers(field_for_ordering, customers)
                if sorted_customers:
                    context['customers'] = sorted_customers
                    return context

        if self.request.method == 'POST':
            first_name = self.request.POST.get('first_name', None)
            last_name = self.request.POST.get('last_name', None)

            if first_name and last_name:
                customers = customers.filter(user__first_name=first_name, user__last_name=last_name)
            elif first_name:
                customers = customers.filter(user__first_name=first_name)
            elif last_name:
                customers = customers.filter(user__last_name=last_name)

        context['customers'] = customers
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CustomersCreateView(View):
    user_form_class = UserCustomerForm
    customer_form_class = CustomerForm

    template_name = 'customers_create.html'

    def get(self, request, *args, **kwargs):

        return render(request,
                      self.template_name,
                      {'user_form': self.user_form_class, 'customer_form': self.customer_form_class}
                      )

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
        return render(request,
                      self.template_name,
                      {'form': self.form_class}
                      )

    def post(self, request, *args, **kwargs):
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            if is_passwords_match(user_form):
                user_cleaned_data = user_form.cleaned_data
                user = authenticate(username=user_cleaned_data['username'], password=user_cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('customers-list')
                else:
                    msg = 'Invalid login or password'
                    user_form.errors['__all__'] = user_form.error_class([msg])

        return render(request, self.template_name, {'form': user_form})
