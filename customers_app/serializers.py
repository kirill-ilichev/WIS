from rest_framework import serializers

from customers_app.models import *


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'points')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CustomerListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Customer
        fields = ('age', 'date_of_birth', 'user')


class CustomerDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    photo = PhotoSerializer()

    class Meta:
        model = Customer
        fields = ('age', 'date_of_birth', 'user', 'photo',)

    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()

        if validated_data.get('user', None):
            user = User.objects.get(id=instance.user_id)
            user.first_name = validated_data.get('user').get('first_name', user.first_name)
            user.last_name = validated_data.get('user').get('last_name', user.last_name)
            user.save()

        if validated_data.get('photo', None):
            photo = Photo.objects.get(id=instance.photo_id)
            photo.photo = validated_data.get('photo').get('photo', photo.photo)
            photo.save()

        return instance
