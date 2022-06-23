from django.contrib import admin
from users.models import User, UserTier
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from images.admin import ImageAdminInline


class CustomUserAdmin(UserAdmin):
    model = User

    inlines = (ImageAdminInline,)
    list_display = (
        "email",
        "pk",
        "username",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = ("date_joined", "last_login", "tier_settings_hash")

    list_filter = (
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_tier",
                    "email",
                    "password",
                    "username",
                    "tier_settings_hash",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "birth_date",
                    "first_name",
                    "last_name",
                    "address",
                    "city",
                    "about_me",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_superuser", "is_staff")}),
        ("Other", {"fields": ("last_login", "date_joined", "receive_newsletter")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user_tier",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
    )
    ordering = ("pk",)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserTier)
admin.site.unregister(Group)
