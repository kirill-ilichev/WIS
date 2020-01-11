from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, DetailView, DeleteView

from customers_app.forms import LoginForm, UserCreateForm, CustomerForm
from customers_app.helpers import are_passwords_match, filter_and_sort_customers_by_query_params
from customers_app.models import Customer, Photo

URLS = {
    'home_url': reverse_lazy('home'),
    'list_url': reverse_lazy('customers-list'),
    'voting_url': reverse_lazy('customers-voting'),
    'auth_url': reverse_lazy('customers-auth'),
    'logout_url': reverse_lazy('customers-logout'),
    'create_url': reverse_lazy('customers-create'),
}


class HomePage(TemplateView):
    """
    Render home page with links to pages of project
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'list_url': URLS['list_url'],
            'voting_url': URLS['voting_url'],
            'auth_url': URLS['auth_url'],
            'create_url': URLS['create_url']
        })

        user = self.request.user
        if user.is_authenticated:
            context['detail_url'] = reverse_lazy('customers-detail', kwargs={'pk': user.customer.id})

        return context


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
        if not self.request.user.is_authenticated:
            raise PermissionDenied

        context = super().get_context_data(**kwargs)
        context.update({
            'photos': Photo.objects.all(),
            'max_points': Photo.max_points
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        photo = get_object_or_404(Photo, pk=request.POST.get('id_of_photo'))
        photo.add_point()

        return self.render_to_response(context)


class CustomersListView(TemplateView):
    """
    Render template with information about customers
    Allows filter and sort customer's information by buttons
    """
    template_name = "customers_list.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied

        context = super().get_context_data(**kwargs)

        customers = Customer.objects.all()
        query_params = self.request.GET

        context['customers'] = filter_and_sort_customers_by_query_params(query_params, customers)
        return context


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
        pk = self.get_object().pk

        context.update({
            'delete_url': reverse_lazy('customers-delete', kwargs={'pk': pk}),
            'logout_url': URLS['logout_url']
        })
        return context


class CustomersDeleteView(DeleteView):
    """
    Delete certain customer
    """
    template_name = 'customers_confirm_delete.html'
    model = Customer
    success_url = URLS['home_url']

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise PermissionDenied

        obj = super().get_object()
        if self.request.user.is_staff:
            return obj

        if self.request.user.customer != obj:
            raise PermissionDenied

        return obj


class CustomersCreateView(View):
    """
    Render registration template
    """
    user_form_class = UserCreateForm
    customer_form_class = CustomerForm

    template_name = 'customers_create.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        return render(request,
                      self.template_name,
                      {'user_form': self.user_form_class,
                       'customer_form': self.customer_form_class,
                       'auth_url': URLS['auth_url']
                       }
                      )

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        user_form = UserCreateForm(request.POST)

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
                      {'form': self.form_class, 'create_url': URLS['create_url']}
                      )

    def post(self, request, *args, **kwargs):
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            if are_passwords_match(user_form):
                user_cleaned_data = user_form.cleaned_data
                user = authenticate(username=user_cleaned_data['username'], password=user_cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    msg = 'Invalid login or password'
                    user_form.errors['__all__'] = user_form.error_class([msg])

        return render(request, self.template_name, {'form': user_form})
