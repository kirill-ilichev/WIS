from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import settings
from customers_app.views import CustomersListView, CustomersCreateView, CustomersAuthView, CustomersDetailView,\
                                export_customers_details_in_xlsx, CustomersVotingView, CustomersVotingAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', CustomersListView.as_view(), name='customers-list'),
    path('customers/auth/', CustomersAuthView.as_view(), name='customers-auth'),
    path('customers/create/', CustomersCreateView.as_view(), name='customers-create'),
    path('customers/<int:pk>/', CustomersDetailView.as_view(), name='customers-detail'),
    path('customers/export/', export_customers_details_in_xlsx),
    path('customers/voting/', CustomersVotingView.as_view(), name='customers-voting'),
    path('api/customers/voting/', CustomersVotingAPIView.as_view(), name='api-customers-voting')
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
