from django.contrib import admin
from django import forms
from .models import User, UserTier
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'size': '30'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'size': '40'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label='is_staff', required=False, initial=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'size': '30'}))
    is_staff = forms.BooleanField(label='is_staff', widget=forms.CheckboxInput, required=False)

    class Meta:
        model = User
        # co jesli dasz tu __all__?
        fields = ('username', 'email', 'password', 'is_staff')


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    model = User

    list_display = (
        "email",
        "pk",
        "username",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = ('date_joined', 'last_login', 'tier_settings_hash')

    list_filter = ('is_superuser', )
    fieldsets = (
        (None, {'fields': ('user_tier', 'email', 'password', 'username', 'tier_settings_hash')}),
        ('Personal info', {'fields': ('birth_date', 'first_name', 'last_name', 'address', 'city', 'about_me')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Other', {'fields': ('last_login', 'date_joined', 'receive_newsletter')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_tier', 'username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'username',)
    ordering = ("email", "pk",)
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
