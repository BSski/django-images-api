import os
import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse

from images.validators import FileValidator
from users.models import User


def content_file_name(instance, filename):
    """Save the file in `images/` directory with a new name."""
    original_extension = filename.split(".")[-1]
    return f"images/{instance.owner.id}_{instance.file_uuid}.{original_extension}"


class Image(models.Model):
    """A model for the app's images."""

    name = models.CharField(
        validators=[
            MinLengthValidator(3, "The field must contain at least 3 characters")
        ],
        max_length=255,
        unique=True,
    )
    file_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to=content_file_name,
        validators=[
            FileValidator(
                max_size=1920 * 1080, content_types=("image/jpeg", "image/png")
            )
        ],
    )
    original_image_link = models.CharField(
        max_length=2500, default="", blank=True, null=True
    )
    thumbnails_links = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f'{self.id}, {self.owner}: "{self.name}"'

    def _create_thumbnails_links(self, thumbnails_sizes, thumbnails_links, file_name):
        """Create new thumbnails links."""
        if thumbnails_sizes is None:
            thumbnails_sizes = []

        if thumbnails_links is None:
            thumbnails_links = {}

        unique_thumbnails_sizes = set(map(str, thumbnails_sizes))
        if set(thumbnails_links.keys()) == unique_thumbnails_sizes:
            return thumbnails_links
        print("\n\n\n type:", type(file_name))

        def _get_link(size):
            return "{}{}".format(
                os.environ.get(
                    "HOSTING_NAME",
                    "{}:{}".format("http://localhost", os.environ.get("PORT")),
                ),
                reverse("images:create_temp_thumbnail_link", args=[size, file_name]),
            )

        new_thumbnails_links = {
            size: thumbnails_links.get(size, _get_link(size))
            for size in unique_thumbnails_sizes
        }

        return new_thumbnails_links

    def update_thumbnails(self, thumbnails_sizes):
        """Update links to thumbnails."""
        original_extension = self.image.name.split(".")[-1]
        file_name = f"{self.owner.id}_{self.file_uuid}.{original_extension}"

        self.thumbnails_links = self._create_thumbnails_links(
            thumbnails_sizes, self.thumbnails_links, file_name
        )
        super().save()

    def save(self, *args, **kwargs):
        """Custom save method. Adds generated thumbnails links to its links field."""
        original_extension = self.image.name.split(".")[-1]
        file_name = f"{self.owner.id}_{self.file_uuid}.{original_extension}"

        thumbnails_sizes = self.owner.user_tier.thumbnails_sizes["sizes"]

        self.thumbnails_links = self._create_thumbnails_links(
            thumbnails_sizes, self.thumbnails_links, file_name
        )

        self.original_image_link = "{}{}".format(
            os.environ.get(
                "HOSTING_NAME",
                "{}:{}".format("http://localhost", os.environ.get("PORT")),
            ),
            reverse("images:create_temp_original_image_link", args=[file_name]),
        )

        super().save(*args, **kwargs)
