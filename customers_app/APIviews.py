from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from customers_app.helpers import filter_and_sort_customers_by_query_params
from customers_app.permissions import IsOwnerOrAdminOrReadOnly
from customers_app.serializers import *
from customers_app.models import Customer, Photo


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

    sort-name= first_name|last_name|age|date_of_birth|username & - sort queryset by 1 of this fields
    sort-direction= asc|desc - chose direction for sorting queryset
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    authentication_classes = [JWTAuthentication]
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
            "username": string,
            "first_name": string,
            "last_name": string
        },
        "photo": {
            "photo": url,
            "points": int
        }
    }

    PUT, PATCH - Update info about customer:
    {
        "date_of_birth": date,
        "first_name": str,
        "last_name": str,
        "username": str
        "photo": file,
    }

    DELETE - Delete customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)

    def perform_destroy(self, instance):
        instance.user.delete()
        instance.photo.delete()
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        user_serializer = UserListSerializer(instance.user, data=request.data, partial=partial)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)

        if bool(request.FILES):
            if instance.photo:
                "If customer had photo before"
                photo_serializer = PhotoSerializer(instance.photo, data=request.FILES, partial=partial)
                photo_serializer.is_valid(raise_exception=True)
                self.perform_update(photo_serializer)
            else:
                photo_serializer = PhotoSerializer(data=request.FILES)
                photo_serializer.is_valid(raise_exception=True)
                self.perform_update(photo_serializer)

                photo = photo_serializer.instance
                instance.photo = photo
                instance.photo_id = photo.id

        customer_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        customer_serializer.is_valid(raise_exception=True)
        self.perform_update(customer_serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(customer_serializer.data)


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
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        if request.data.get('id_of_photo', None):
            photo = get_object_or_404(Photo, pk=request.data.get('id_of_photo'))
            photo.add_point()
        return self.list(request, *args, **kwargs)


class CustomersCreateAPIView(CreateAPIView):
    """
    POST - Create customer
    {
        "date_of_birth": date,
        "first_name": "string",
        "last_name": "string",
        "username": "string"
        "password": "string",
        "confirm_password": "string",
        "photo": file
    }
    """
    permission_classes = (IsAdminUser, )
    serializer_class = CustomerCreateSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):

        user_serializer = UserListSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        photo_serializer = PhotoSerializer(data=request.FILES)
        photo_serializer.is_valid(raise_exception=True)

        customer_serializer = CustomerCreateSerializer(data=request.data)
        customer_serializer.is_valid(raise_exception=True)

        self.perform_create(user_serializer)
        self.perform_create(photo_serializer)

        customer_serializer.validated_data.update({"user": user_serializer.instance,
                                                   "photo": photo_serializer.instance})

        self.perform_create(customer_serializer)

        headers = self.get_success_headers(customer_serializer.data)

        return Response(customer_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
