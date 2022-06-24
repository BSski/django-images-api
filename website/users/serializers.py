from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Simple serializer for User model."""

    class Meta:
        model = User
        fields = [
            "id",
            "user_tier",
            "email",
            "username",
            "first_name",
            "last_name",
            "address",
            "city",
            "about_me",
            "birth_date",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        ]
        depth = 1


class UserDetailsSerializer(serializers.ModelSerializer):
    """Simple serializer for User model w/o password."""

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "is_staff",
            "city",
            "about_me",
            "profile_image",
        )
        read_only_fields = ("username",)
