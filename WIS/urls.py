from django.contrib import admin
from django.urls import path

from customers_app.views import CustomersListView, CustomersCreateView, CustomersAuthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', CustomersListView.as_view(), name='customers-list'),
    path('customers/auth/', CustomersAuthView.as_view(), name='customers-auth'),
    path('customers/create/', CustomersCreateView.as_view(), name='customers-create'),
]
