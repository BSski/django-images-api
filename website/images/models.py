from django.db import models
from users.models import User
from PIL import Image as Img
from django.core.validators import MinLengthValidator
from .validators import FileValidator
from django.urls import reverse
import time


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return f"images/{instance.owner.id}_{str(time.time()).replace('.', '')}.{ext}"


class Image(models.Model):
    name = models.CharField(
        validators=[
            MinLengthValidator(2, "The field must contain at least 2 characters")
        ],
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    image = models.ImageField(
        upload_to=content_file_name,
        validators=[
            FileValidator(
                max_size=1920 * 1080, content_types=("image/jpeg", "image/png")
            )
        ]
    )
    original_image_link = models.CharField(max_length=2500, default="", blank=True, null=True)
    thumbnails_links = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f'{self.id}, {self.owner}: "{self.name}"'

    def update_thumbnails(self, thumbnails_sizes):
        if thumbnails_sizes is None:
            thumbnails_sizes = []

        if self.thumbnails_links is None:
            self.thumbnails_links = {}

        unique_thumbnails_sizes = set(map(str, thumbnails_sizes))
        if set(self.thumbnails_links.keys()) == unique_thumbnails_sizes:
            return

        new_thumbnails_links = {
            size: self.thumbnails_links.get(size, "")
            for size in unique_thumbnails_sizes
        }

        self.thumbnails_links = new_thumbnails_links
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thumbnail_sizes = self.owner.user_tier.thumbnails_sizes["sizes"]
        if not self.thumbnails_links:
            self.thumbnails_links = {}
        for size in thumbnail_sizes:
            self.thumbnails_links[size] = reverse(
                "get_or_create_thumbnail_link",
                args=[size, self.image.name.split('/')[1]]
            )

        self.original_image_link = reverse(
            "create_temporary_original_image_link",
            args=[self.image.name.split('/')[1]]
        )
        super().save(*args, **kwargs)
