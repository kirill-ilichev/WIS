from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers

from customers_app.models import *


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'points')
        read_only_fields = ('points', )


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True}}


class CustomerListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'age', 'date_of_birth', 'user')
        read_only_fields = ('age', )


class CustomerSerializer(CustomerListSerializer):
    photo = PhotoSerializer(read_only=True)

    class Meta(CustomerListSerializer.Meta):
        fields = CustomerListSerializer.Meta.fields + ('photo', )


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
        photo = validated_data.pop('photo')

        user = validated_data.pop('user')
        user.set_password(validated_data.pop('password'))
        user.save()

        validated_data.pop('confirm_password')

        customer = Customer.objects.create(user=user, photo=photo, **validated_data)
        return customer
