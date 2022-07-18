import boto3

from django.test import TestCase
from django.urls import reverse, resolve

from users.models import User, UserTier

from website import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.enterprise_user_tier = UserTier.objects.create(
            pk=5,
            name="Enterprise",
            thumbnails_sizes={"sizes": [200, 400]},
            can_use_original_image_link=1,
            can_fetch_expiring_link=1,
            settings_hash="r8ls6w",
        )
        cls.enterprise_user = User.objects.create_user(
            id=1,
            username="test_user",
            email="test@test.com",
            password="test",
            user_tier=cls.enterprise_user_tier,
        )
        cls.s3_client = boto3.client(
            "s3",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
            endpoint_url=settings.LOCALSTACK_ENDPOINT_URL,
        )
        cls.s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

    # def setUp(self):
    #     self.client.force_login(self.enterprise_user)

    @property
    def bearer_token(self):
        user = self.enterprise_user
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    # def test_initial_s3_bucket_is_empty(self):
    #     s3_objects = ImageModelTest.s3_client.list_objects_v2(
    #         Bucket=settings.AWS_STORAGE_BUCKET_NAME
    #     )
    #     self.assertEqual("Contents" in s3_objects, False)

    def test_image_can_be_uploaded_to_s3_bucket(self):
        # factory = APIRequestFactory()
        # with open("images/tests/files/png_image.png", "rb") as test_image:
        #     url = reverse("images:api-root") + "images/"
        #     request = factory.post(
        #         url,
        #         {"name": "test_image", "image": test_image},
        #         **self.bearer_token,
        #     )
        #     view = resolve(url).func
        #     response = view(request)
        #     response.render()

        ImageModelTest.s3_client.upload_file(
            "images/tests/files/png_image.png",
            settings.AWS_STORAGE_BUCKET_NAME,
            "images/test_image.png",
            ExtraArgs={"ContentType": "image/png"},
        )

        s3_objects = ImageModelTest.s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME
        )
        self.assertEqual("Contents" in s3_objects, True)
