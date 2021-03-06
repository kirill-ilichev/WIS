from django.urls import path

from .export_functions import export_customers_details_in_xlsx
from .views import *

urlpatterns = [
    path('auth/', CustomersAuthView.as_view(), name='customers-auth'),
    path('logout/', logout_view, name='customers-logout'),
    path('create/', CustomersCreateView.as_view(), name='customers-create'),
    path('export/', export_customers_details_in_xlsx, name='customers-export'),
    path('list/', CustomersListView.as_view(), name='customers-list'),
    path('voting/', CustomersVotingView.as_view(), name='customers-voting'),
    path('<int:pk>/', CustomersDetailView.as_view(), name='customers-detail'),
    path('<int:pk>/delete/', CustomersDeleteView.as_view(), name='customers-delete')
]
