from django import forms
from images.models import Image


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
        fields = ["name", "image", "owner", "original_image_link", "thumbnails_links"]


class CustomInlineImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "name",
            "image",
        ]
