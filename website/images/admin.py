from django.contrib import admin
from .models import Image
from .forms import CustomImageForm, CustomAddImageForm, CustomInlineImageForm


class ImageAdminInline(admin.TabularInline):
    model = Image
    form = CustomInlineImageForm
    readonly_fields = ('image',)

    def has_add_permission(self, request, *args, **kwargs):
        return False


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = CustomImageForm
    add_form = CustomAddImageForm

    list_display = (
        "name",
        "id",
        "owner"
    )
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
            defaults['form'] = self.add_form
        defaults |= kwargs
        return super().get_form(request, obj, **defaults)

    def get_readonly_fields(self, request, obj=None):
        """Set Image field to read-only during editing."""
        return self.readonly_fields + ('image', ) if obj else self.readonly_fields
