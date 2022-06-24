from rest_framework import serializers
from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """Simple serializer for Image model."""

    owner = serializers.HyperlinkedRelatedField(
        view_name="users:detail", read_only=True
    )

    class Meta:
        model = Image
        fields = [
            "id",
            "file_uuid",
            "name",
            "image",
            "original_image_link",
            "thumbnails_links",
            "owner",
        ]


class AddImageSerializer(serializers.ModelSerializer):
    """Simple serializer for adding new images in images viewset form."""

    class Meta:
        model = Image
        fields = ["name", "image"]
