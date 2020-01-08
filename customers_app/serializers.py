from rest_framework import serializers

from customers_app.models import *


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'points')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CustomerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('age', 'date_of_birth', 'user')


class CustomerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    photo = PhotoSerializer()

    class Meta:
        model = Customer
        fields = ('age', 'date_of_birth', 'user', 'photo',)
