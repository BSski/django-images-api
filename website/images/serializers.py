from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    #creator = serializers.ReadOnlyField(source='creator.username')
    #creator_id = serializers.ReadOnlyField(source='creator.id')
    #image_url = serializers.ImageField(required=False)

    #user_details = serializers.HyperlinkedIdentityField()
    #https://www.youtube.com/watch?v=1MKnL8WhaYw

    class Meta:
        model = Image
        fields = ['name', 'image', 'original_image_link', 'thumbnails_links', 'owner']
        depth = 1