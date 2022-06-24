from django import forms
from users.models import UserTier


class CustomAddUserTierForm(forms.ModelForm):
    """Custom form for adding new UserTier objects."""

    class Meta:
        model = UserTier
        fields = [
            "name",
            "thumbnails_sizes",
            "can_use_original_image_link",
            "can_fetch_expiring_link",
        ]


class CustomUserTierForm(forms.ModelForm):
    """Custom form for viewing and editing UserTier objects."""

    class Meta:
        model = UserTier
        fields = [
            "name",
            "thumbnails_sizes",
            "can_use_original_image_link",
            "can_fetch_expiring_link",
        ]
