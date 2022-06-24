from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from hashids import Hashids


class UserTier(models.Model):
    """A model for the user tiers."""

    name = models.CharField(max_length=250)
    thumbnails_sizes = models.JSONField(default=dict)
    can_use_original_image_link = models.BooleanField(default=False)
    can_fetch_expiring_link = models.BooleanField(default=False)
    settings_hash = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.id}. {self.name}"

    def save(self, *args, **kwargs):
        """
        Custom save method. Generates a hash basing on current thumbnail sizes and
        checks whether they were changed in the current edit action. If they did,
        it updates the sizes links of all Users who are in this UserTier.
        """
        hashids = Hashids()
        hashed_settings = hashids.encode(*(*self.thumbnails_sizes.get("sizes", []),))
        settings_changed = self.settings_hash != hashed_settings
        if settings_changed:
            self.settings_hash = hashed_settings

        super().save(*args, **kwargs)

        if settings_changed:
            for user in self.users.all():
                user.save()


class UserManager(BaseUserManager):
    """A manager for the custom user model."""

    def _create_user(
        self,
        username,
        email,
        password,
        is_active,
        is_staff,
        is_superuser,
        **extra_fields,
    ):
        if not username:
            raise ValueError("The given username is not valid.")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=timezone.now(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        """Creates and saves a User with the given email and password."""
        return self._create_user(
            username,
            email,
            password,
            is_active=True,
            is_staff=False,
            is_superuser=False,
            **extra_fields,
        )

    def create_superuser(self, username, email, password, **extra_fields):
        """Creates and saves a superuser with the given email and password."""
        return self._create_user(
            username,
            email,
            password,
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """A custom User model."""

    user_tier = models.ForeignKey(
        UserTier, on_delete=models.SET_NULL, null=True, related_name="users", default=3
    )
    tier_settings_hash = models.CharField(max_length=1000, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    about_me = models.TextField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_readonly_superuser = models.BooleanField(default=False)
    receive_newsletter = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def _update_images(self):
        """Update all images' thumbnails links."""
        for image in self.images.all():
            image.update_thumbnails(self.user_tier.thumbnails_sizes.get("sizes"))

    def _update_tier_settings_hash(self):
        """Update settings hash of this user's UserTier."""
        self.tier_settings_hash = self.user_tier.settings_hash

    def save(self, *args, **kwargs):
        """
        Custom save method. Checks whether this user's UserTier changed via checking its
        settings hash. If it did, updates its images thumbnails links.
        """
        tier_changed = self.tier_settings_hash != self.user_tier.settings_hash
        self._update_tier_settings_hash()
        if tier_changed:
            self._update_images()
        super().save(*args, **kwargs)
