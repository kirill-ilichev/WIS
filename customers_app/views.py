from io import BytesIO
from xlwt import Workbook

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View, TemplateView, DetailView
from django.urls import reverse
from rest_framework.generics import ListAPIView

from customers_app.forms import CustomerForm,  UserCustomerForm, LoginForm
from customers_app.helpers import are_passwords_match, get_model_fields_list,\
                                  add_point_to_photo, filter_and_sort_customers_by_query_params
from customers_app.models import Customer, Photo
from customers_app.serializers import PhotoSerializer, CustomerListSerializer


class CustomersListAPIView(ListAPIView):
    """
    GET - Returns info about customers
    [
        {
        "age": int,
        "date_of_birth": date,
        "user": {
            "first_name": string,
            "last_name": string
        },
        ...

    ]
    Use query params for sorting and filtering
    ?first-name= <string> & - filter queryset by first name of customer
    last-name= <string> - filter queryset by last name of customer

    sort-name= first_name|last_name|age|date_of_birth & - sort queryset by 1 of 4 fields
    sort-direction= asc|desc - chose direction for sorting queryset
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        if not query_params:
            return self.list(request, *args, **kwargs)

        queryset = filter_and_sort_customers_by_query_params(query_params, self.queryset)
        self.queryset = queryset

        return self.list(request, *args, **kwargs)


class CustomersVotingAPIView(ListAPIView):
    """
    GET - Returns info about all photos
    [
        {
            "id": int,
            "photo": url,
            "points": int,
        },
        ...
    ]
    POST - Add point to certain photo
    {"id_of_photo": <int:id of photo>}
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def post(self, request, *args, **kwargs):
        if request.data.get('id_of_photo', None):
            add_point_to_photo(request.data.get('id_of_photo'))
        return self.list(request, *args, **kwargs)


class CustomersVotingView(TemplateView):
    """
    Render template with photos and points for each photo.
    Allows to vote for certain photo by click on button near photo's points
    """
    template_name = "customers_voting.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['photos'] = Photo.objects.all()
        context['max_points'] = Photo.max_points

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        add_point_to_photo(request.POST.get('id_of_photo'))

        return self.render_to_response(context)


class CustomersListView(TemplateView):
    """
    Render template with information about customers
    Allows filter and sort customer's information by buttons
    """
    template_name = "customers_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

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


class CustomersCreateView(View):
    """
    Render registration template
    """
    user_form_class = UserCustomerForm
    customer_form_class = CustomerForm

    template_name = 'customers_create.html'

    def get(self, request, *args, **kwargs):

        return render(request,
                      self.template_name,
                      {'user_form': self.user_form_class, 'customer_form': self.customer_form_class}
                      )

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user_form = UserCustomerForm(request.POST)

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
                    return redirect('customers-list')
                else:
                    msg = 'Invalid login or password'
                    user_form.errors['__all__'] = user_form.error_class([msg])

        return render(request, self.template_name, {'form': user_form})


def export_customers_details_in_xlsx(request):
    """
    Collects information about customers and export it in xlsx file.
    Then allows customer to chose where to save export file
    """
    excelfile = BytesIO()

    wb = Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheetname')

    fields_for_writing = ['first_name', 'last_name', 'age', 'date_of_birth']
    for col, field in enumerate(fields_for_writing):
        ws.write(0, col, field)

    customers = Customer.objects.all()
    for row, customer in enumerate(customers, 1):
        for col, field in enumerate(fields_for_writing):
            if field in get_model_fields_list(User):
                ws.write(row, col, getattr(customer.user, field))
            else:
                ws.write(row, col, getattr(customer, field))

    wb.save(excelfile)

    response = HttpResponse(excelfile.getvalue())
    response['Content-Type'] = 'application/x-download'
    response['Content-Disposition'] = 'attachment;filename=table.xlsx'

    return response
