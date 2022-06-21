from django.contrib import admin
from .models import User, UserTier
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    model = User

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

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #
    #     is_superuser = request.user.is_superuser
    #     if not is_superuser:
    #         form.base_fields['username'].disabled = True
    #         form.base_fields['is_superuser'].disabled = True
    #         form.base_fields['user_permissions'].disabled = True
    #         form.base_fields['groups'].disabled = True
    #     return form


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserTier)
admin.site.unregister(Group)
