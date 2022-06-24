from django import forms

from images.models import Image


class CustomAddImageForm(forms.ModelForm):
    """Custom form for adding new Image objects."""

    class Meta:
        model = Image
        fields = [
            "name",
            "image",
            "owner",
        ]


class CustomImageForm(forms.ModelForm):
    """Custom form for viewing and editing Image objects."""

    class Meta:
        model = Image
        fields = ["name", "image", "owner", "original_image_link", "thumbnails_links"]


class CustomInlineImageForm(forms.ModelForm):
    """Custom form for viewing and editing Image objects inline."""

    class Meta:
        model = Image
        fields = [
            "name",
            "image",
        ]
