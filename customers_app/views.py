from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, DetailView, DeleteView

from customers_app.forms import CustomerForm,  UserForm, LoginForm
from customers_app.helpers import are_passwords_match, add_point_to_photo, filter_and_sort_customers_by_query_params
from customers_app.models import Customer, Photo


def logout_view(request):
    logout(request)
    return redirect('customers-auth')


class CustomersVotingView(TemplateView):
    """
    Render template with photos and points for each photo.
    Allows to vote for certain photo by click on button near photo's points
    """
    template_name = "customers_voting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['photos'] = Photo.objects.all()
        context['max_points'] = Photo.max_points

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        context = self.get_context_data(**kwargs)

        add_point_to_photo(request.POST.get('id_of_photo'))

        return self.render_to_response(context)


class CustomersListView(TemplateView):
    """
    Render template with information about customers
    Allows filter and sort customer's information by buttons
    """
    template_name = "customers_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customers = Customer.objects.all()
        query_params = self.request.GET

        context['customers'] = filter_and_sort_customers_by_query_params(query_params, customers)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CustomersDetailView(DetailView):
    """
    Render template with information about certain customer
    """
    template_name = "customers_detail.html"
    model = Customer

    def get_object(self, queryset=None):

        if not self.request.user.is_authenticated:
            raise PermissionDenied

        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url'] = reverse_lazy('customers-delete', kwargs={'pk': self.get_object().pk})
        context['logout_url'] = reverse_lazy('customers-logout')
        return context


class CustomersDeleteView(DeleteView):
    """
    Delete certain customer
    """
    template_name = 'customers_confirm_delete.html'
    model = Customer
    success_url = reverse_lazy('customers-auth')

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise PermissionDenied

        obj = super().get_object()
        if self.request.user.is_staff:
            return obj

        if not self.request.user.customer == obj:
            raise PermissionDenied

        return obj


class CustomersCreateView(View):
    """
    Render registration template
    """
    user_form_class = UserForm
    customer_form_class = CustomerForm

    template_name = 'customers_create.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        return render(request,
                      self.template_name,
                      {'user_form': self.user_form_class, 'customer_form': self.customer_form_class}
                      )

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        user_form = UserForm(request.POST)

        customer_form = CustomerForm(request.POST, request.FILES or None)
        if user_form.is_valid() and customer_form.is_valid():
            if are_passwords_match(user_form):
                user_cleaned_data = user_form.cleaned_data
                user_cleaned_data.pop('confirm_password')

                user = User.objects.create_user(**user_cleaned_data)
                customer = customer_form.save(commit=False)

                photo = Photo.objects.create(photo=request.FILES['photo'])

                customer.user = user
                customer.photo = photo

                customer.save()

                return HttpResponseRedirect(reverse('customers-detail', kwargs={'pk': customer.pk}))

        return render(request, self.template_name, {'user_form': user_form, 'customer_form': customer_form})


class CustomersAuthView(View):
    """
    Render authentication template
    """
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
            if are_passwords_match(user_form):
                user_cleaned_data = user_form.cleaned_data
                user = authenticate(username=user_cleaned_data['username'], password=user_cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('customers-detail', pk=user.customer.pk)
                else:
                    msg = 'Invalid login or password'
                    user_form.errors['__all__'] = user_form.error_class([msg])

        return render(request, self.template_name, {'form': user_form})
