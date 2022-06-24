from rest_framework import serializers

from users.models import User


class UsersDetailSerializer(serializers.ModelSerializer):
    """Simple serializer for User model."""

    class Meta:
        model = User
        fields = [
            "id",
            "user_tier",
            "tier_settings_hash",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "city",
            "about_me",
            "birth_date",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_readonly_superuser",
            "receive_newsletter",
        ]
        depth = 1
