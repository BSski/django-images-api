from django import forms
from .models import Image


class CustomAddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "name",
            "image",
            "owner",
        ]


class CustomImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "name",
            "image",
            "owner",
            "original_image_link",
            "thumbnails_links"
        ]
