from django.contrib import admin
from users.models import User, UserTier
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from images.admin import ImageAdminInline
from users.forms import CustomAddUserTierForm, CustomUserTierForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model custom admin."""

    model = User
    inlines = (ImageAdminInline,)
    list_display = (
        "email",
        "pk",
        "username",
        "is_staff",
        "is_superuser",
        "is_readonly_superuser",
    )
    readonly_fields = ("date_joined", "last_login", "tier_settings_hash")
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_readonly_superuser",
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
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "is_readonly_superuser",
                )
            },
        ),
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
                    "is_readonly_superuser",
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

    def has_change_permission(self, request, obj=None):
        """Prohibit readonly-superuser from changing User objects."""
        return not request.user.is_readonly_superuser

    def has_add_permission(self, request, obj=None):
        """Prohibit readonly-superuser from adding User objects."""
        return not request.user.is_readonly_superuser

    def has_delete_permission(self, request, obj=None):
        """Prohibit readonly-superuser from deleting User objects."""
        return not request.user.is_readonly_superuser


@admin.register(UserTier)
class UserTierAdmin(admin.ModelAdmin):
    """UserTier model custom admin."""

    form = CustomUserTierForm
    add_form = CustomAddUserTierForm
    list_display = (
        "name",
        "id",
        "thumbnails_sizes",
        "can_use_original_image_link",
        "can_fetch_expiring_link",
    )
    search_fields = ("name",)
    ordering = ("pk",)
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        """Use special form during UserTier creation."""
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults = {**defaults, **kwargs}
        return super().get_form(request, obj, **defaults)

    def get_readonly_fields(self, request, obj=None):
        """Set settings_hash field to read-only during editing."""
        return (
            self.readonly_fields + ("settings_hash",) if obj else self.readonly_fields
        )

    def has_change_permission(self, request, obj=None):
        """Prohibit readonly-superuser from changing UserTier objects."""
        return not request.user.is_readonly_superuser

    def has_add_permission(self, request, obj=None):
        """Prohibit readonly-superuser from adding UserTier objects."""
        return not request.user.is_readonly_superuser

    def has_delete_permission(self, request, obj=None):
        """Prohibit readonly-superuser from deleting UserTier objects."""
        return not request.user.is_readonly_superuser


admin.site.unregister(Group)
