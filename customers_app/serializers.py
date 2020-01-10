from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers

from customers_app.models import *


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'points')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class CustomerListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'age', 'date_of_birth', 'user')


class CustomerSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    photo = PhotoSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'age', 'date_of_birth', 'user', 'photo')


class CustomerCreateSerializer(CustomerSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Confirm password'}
    )

    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields+('password', 'confirm_password')

    def validate(self, data):
        password = data.get('password')

        errors = dict()
        if password != data.get('confirm_password'):
            errors['password'] = ['Passwords doen\'t match']
            raise serializers.ValidationError(errors)

        try:
            password_validation.validate_password(password=password)
        except ValidationError as e:
            errors['password'] = list(e.messages)
            raise serializers.ValidationError(errors)

        return super().validate(data)

    def create(self, validated_data):

        user_data = validated_data.pop('user')

        user = User.objects.create_user(password=validated_data.pop('password'),
                                        **user_data)

        validated_data.pop('confirm_password')
        customer = Customer.objects.create(**validated_data, user=user)

        return customer
