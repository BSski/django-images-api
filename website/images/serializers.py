from rest_framework import serializers
from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "file_uuid",
            "name",
            "image",
            "original_image_link",
            "thumbnails_links",
            "owner",
        ]
        depth = 2


class AddImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "image"]
