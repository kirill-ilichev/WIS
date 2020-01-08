from rest_framework.generics import ListAPIView

from customers_app.helpers import add_point_to_photo, filter_and_sort_customers_by_query_params
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
