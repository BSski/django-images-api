import boto3

from rest_framework import viewsets
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from images.decorators import (
    has_certain_thumbnail_size_permission,
    has_fetch_expiring_link_permission,
    has_use_original_image_link_permission,
)
from images.models import Image
from images.serializers import AddImageSerializer, ImageSerializer
from images.throttles import (
    AnonymousBurstThrottle,
    AnonymousSustainedThrottle,
    GetImagesUserBurstThrottle,
    GetImagesUserSustainedThrottle,
    OriginalImgLinkBurstThrottle,
    OriginalImgLinkSustainedThrottle,
    PostImageUserBurstThrottle,
    PostImageUserSustainedThrottle,
    ThumbnailLinkBurstThrottle,
    ThumbnailLinkSustainedThrottle,
)
from images.utils import (
    check_if_file_exists_in_s3,
    create_new_thumbnail,
    get_s3_client,
    get_temp_thumbnail_link,
)
from images.validators import (
    validate_if_correct_user,
    validate_img_name,
    validate_time_exp,
)
from website import settings


@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    """Default view of the app."""
    return Response(
        {
            "message": "Hi there! You're probably looking for /auth/login/ and /images/ endpoints."
        }
    )


class ImageViewSet(viewsets.ModelViewSet):
    """A viewset for Image model."""

    queryset = Image.objects.all()
    pagination_class = LimitOffsetPagination
    throttle_classes = [
        AnonymousBurstThrottle,
        AnonymousSustainedThrottle,
        PostImageUserBurstThrottle,
        PostImageUserSustainedThrottle,
        GetImagesUserBurstThrottle,
        GetImagesUserSustainedThrottle,
    ]
    serializer_classes = {"create": AddImageSerializer}
    default_serializer_class = ImageSerializer  # Your default serializer

    def get_serializer_class(self):
        """Use a different serializer for posting new image through the form."""
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def perform_create(self, serializer):
        """Add an owner to Image object if created through viewset's form."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """List current user's images."""
        user = self.request.user
        return Image.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        """
        Removes original image link from the returned data. Instead returns a message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"status": "Successfully posted"},
            status=HTTP_201_CREATED,
            headers=headers,
        )


@api_view(["GET"])
@throttle_classes([OriginalImgLinkBurstThrottle, OriginalImgLinkSustainedThrottle])
@has_use_original_image_link_permission
def create_temp_original_image_link(request, img_name):
    """Creates a temporary link to the original version of the requested image."""
    if (img_name_status := validate_img_name(img_name)) != "OK":
        return img_name_status

    if (user_status := validate_if_correct_user(request, img_name)) != "OK":
        return user_status

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    temp_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": f"images/{img_name}",
        },
        ExpiresIn=1800,
    )
    return Response({"original_image_temporary_link": temp_url})


@api_view(["GET"])
@throttle_classes([ThumbnailLinkBurstThrottle, ThumbnailLinkSustainedThrottle])
@has_fetch_expiring_link_permission
@has_certain_thumbnail_size_permission
def create_temp_thumbnail_link(
    request, thumbnail_size, img_name, has_time_exp_permission
):
    """Creates a temporary link to a requested thumbnail size."""
    if (img_name_status := validate_img_name(img_name)) != "OK":
        return img_name_status

    if (user_status := validate_if_correct_user(request, img_name)) != "OK":
        return user_status

    time_exp = request.query_params.get("time_exp", None)
    if time_exp and not has_time_exp_permission:
        return Response(
            {
                "status": "Forbidden: the user is not permitted to specify expiration time of the link."
            },
            status=HTTP_403_FORBIDDEN,
        )
    if time_exp:
        if (time_exp_status := validate_time_exp(time_exp)) != "OK":
            return time_exp_status
    else:
        time_exp = 120

    s3_client = get_s3_client()
    file_exists_in_s3 = check_if_file_exists_in_s3(img_name, thumbnail_size, s3_client)
    if not file_exists_in_s3:
        create_new_thumbnail(thumbnail_size, img_name)
    temp_url = get_temp_thumbnail_link(s3_client, thumbnail_size, img_name, time_exp)
    return Response({"thumbnail_temporary_link": temp_url})
