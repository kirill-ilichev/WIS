from django.urls import path

from .APIviews import CustomersListAPIView, CustomersVotingAPIView
from .export_functions import export_customers_details_in_xlsx
from .views import CustomersListView, CustomersCreateView, CustomersAuthView, CustomersDetailView,\
                   CustomersVotingView

urlpatterns = [
    path('auth/', CustomersAuthView.as_view(), name='customers-auth'),
    path('create/', CustomersCreateView.as_view(), name='customers-create'),
    path('export/', export_customers_details_in_xlsx, name='customers-export'),
    path('list/', CustomersListView.as_view(), name='customers-list'),
    path('voting/', CustomersVotingView.as_view(), name='customers-voting'),
    path('<int:pk>/', CustomersDetailView.as_view(), name='customers-detail'),
    path('api/list/', CustomersListAPIView.as_view(), name='api-customers-list'),
    path('api/voting/', CustomersVotingAPIView.as_view(), name='api-customers-voting'),
]
