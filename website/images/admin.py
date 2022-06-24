from django.contrib import admin
from images.models import Image
from images.forms import CustomImageForm, CustomAddImageForm, CustomInlineImageForm


class ImageAdminInline(admin.TabularInline):
    """Image model custom inline admin."""

    model = Image
    form = CustomInlineImageForm
    extra = 1

    def has_change_permission(self, request, *args, **kwargs):
        """Prohibit anyone from changing Image objects when viewed inline."""
        return False


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Image model custom admin."""

    form = CustomImageForm
    add_form = CustomAddImageForm
    list_display = ("file_uuid", "name", "id", "owner")
    search_fields = (
        "email",
        "username",
    )
    ordering = ("pk",)
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        """Use special form during Image creation."""
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults = {**defaults, **kwargs}
        return super().get_form(request, obj, **defaults)

    def get_readonly_fields(self, request, obj=None):
        """Set Image field to read-only during editing."""
        return (
            self.readonly_fields
            + (
                "image",
                "file_uuid",
            )
            if obj
            else self.readonly_fields
        )

    def has_change_permission(self, request, obj=None):
        """Prohibit readonly-superuser from changing Image objects."""
        return not request.user.is_readonly_superuser

    def has_add_permission(self, request, obj=None):
        """Prohibit readonly-superuser from adding Image objects."""
        return not request.user.is_readonly_superuser

    def has_delete_permission(self, request, obj=None):
        """Prohibit readonly-superuser from deleting Image objects."""
        return not request.user.is_readonly_superuser
