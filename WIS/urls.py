from django.contrib import admin
from django.urls import path

from customers_app.views import CustomersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', CustomersView.as_view())
]
