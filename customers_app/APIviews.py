from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from customers_app.helpers import add_point_to_photo, filter_and_sort_customers_by_query_params
from customers_app.permissions import IsOwnerOrAdminOrReadOnly
from customers_app.models import Customer, Photo
from customers_app.serializers import PhotoSerializer, CustomerListSerializer, CustomerDetailSerializer


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
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        if not query_params:
            return self.list(request, *args, **kwargs)

        queryset = filter_and_sort_customers_by_query_params(query_params, self.queryset)
        self.queryset = queryset

        return self.list(request, *args, **kwargs)


class CustomersDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET - Returns info about customers
    {
        "age": int,
        "date_of_birth": date,
        "user": {
            "first_name": string,
            "last_name": string
        },
        "photo": {
            "id": int,
            "photo": url,
            "points": int
        }
    }
    PUT, PATCH - Update info about customer
    DELETE - Delete customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)
    parser_classes = [parsers.MultiPartParser]

    def perform_destroy(self, instance):
        instance.user.delete()
        instance.photo.delete()
        instance.delete()


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
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        if request.data.get('id_of_photo', None):
            add_point_to_photo(request.data.get('id_of_photo'))
        return self.list(request, *args, **kwargs)
