import boto3

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from images.models import Image

from website import settings


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.test_image = Image.objects.create(
        #     name="TestImage",
        #     image=""
        # )
        cls.test_image = SimpleUploadedFile("testImage.jpg", b"file_content", content_type="image/jpeg")
        cls.s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        )

    def test_initial_s3_bucket_is_empty(self):
        s3_objects = self.s3_client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        self.assertEqual("Contents" in s3_objects, True)

    def test_image_can_be_uploaded_to_s3_bucket(self):
        self.client.post(reverse('images:api-root'), {'image': self.test_image})
        s3_objects = self.s3_client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        self.assertEqual("Contents" in s3_objects, True)



#
# ### example code below
#
# from datetime import date
#
# from django.test import TestCase
#
# from music.models import Author, Song
#
#
# class AuthorModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_author = Author.objects.create(
#             name="TestName",
#             surname="TestSurname",
#         )
#
#     def test_author_str_equals_name_and_surname(self):
#         self.assertEqual(
#             str(self.test_author), f"{self.test_author.name} {self.test_author.surname}"
#         )
#
#
# class SongModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_song = Song.objects.create(
#             title="TestTitle",
#             created_at=date(2022, 6, 8),
#         )
#
#     def test_song_str_equals_song_title(self):
#         self.assertEqual(str(self.test_song), self.test_song.title)
#
#     def test_song_has_an_author(self):
#         test_author = Author.objects.create(
#             name="TestName",
#             surname="TestSurname",
#         )
#         self.test_song.authors.set([test_author])
#         self.assertEqual(self.test_song.authors.count(), 1)
