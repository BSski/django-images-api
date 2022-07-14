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
        cls.test_image = SimpleUploadedFile(
            "testImage.jpg", b"file_content", content_type="image/jpeg"
        )
        cls.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.LOCALSTACK_ENDPOINT_URL,
        )

    def test_initial_s3_bucket_is_empty(self):
        s3_objects = ImageModelTest.s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME
        )
        self.assertEqual("Contents" in s3_objects, False)

    def test_image_can_be_uploaded_to_s3_bucket(self):
        # Need authentication for posting to this endpoint.
        # with open('images/tests/files/png_image.png', 'rb') as test_image:
        #     response = self.client.post(
        #         reverse("images:api-root")+"images/", {"image": test_image}
        #     )
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.LOCALSTACK_ENDPOINT_URL,
        )
        s3_client.upload_file(
            'images/tests/files/png_image.png',
            settings.AWS_STORAGE_BUCKET_NAME,
            "images/test_image.png",
            ExtraArgs={'ContentType': "image/png"}
        )
        s3_objects = s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME
        )
        self.assertEqual("Contents" in s3_objects, True)
