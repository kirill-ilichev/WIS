from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from customers_app.APIviews import *
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customers_app.urls')),
    path('api/customers/', include([
        path('list/', CustomersListAPIView.as_view(), name='api-customers-list'),
        path('voting/', CustomersVotingAPIView.as_view(), name='api-customers-voting'),
        path('<int:pk>/', CustomersDetailAPIView.as_view(), name='api-customers-detail')
    ]))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
