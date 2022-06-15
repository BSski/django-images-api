from django.db import models
from users.models import User


class Image(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    original_image_link = models.CharField(max_length=2500)
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
