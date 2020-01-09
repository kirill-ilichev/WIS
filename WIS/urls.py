from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from customers_app.APIviews import *
from customers_app.views import HomePage
from . import settings

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('customers/', include('customers_app.urls')),
    path('api/customers/', include([
        path('list/', CustomersListAPIView.as_view(), name='api-customers-list'),
        path('create/', CustomersCreateAPIView.as_view(), name='api-customers-create'),
        path('voting/', CustomersVotingAPIView.as_view(), name='api-customers-voting'),
        path('<int:pk>/', CustomersDetailAPIView.as_view(), name='api-customers-detail')
    ]))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
