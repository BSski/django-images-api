from django.contrib import admin
from .models import Image
from django import forms


# admin.site.register(Image)


# forms.py


class CustomImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "name",
            "image",
            "owner",
        ]
        widgets = {
            "a": forms.TextInput(),
        }


# admin.py
# from app.forms import CustomImageForm


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    form = CustomImageForm


# SPRAWDZ CZY TEN CUSTOM IMAGE FORM WGL DZIALA BO CHYBA NIC NIE ZMIENIA
