from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "image", "original_image_link", "thumbnails_links", "owner"]
        depth = 2
