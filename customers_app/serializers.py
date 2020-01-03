from rest_framework import serializers

from customers_app.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    send_post_to_vote_for_this_photo = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'points', 'send_post_to_vote_for_this_photo')

    def get_send_post_to_vote_for_this_photo(self, obj):
        if obj.points == Photo.max_points:
            return "This photo has max of points"

        return "{'id_of_photo': %d}" % obj.id
