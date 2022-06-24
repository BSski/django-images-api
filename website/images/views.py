import boto3

from django.core.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.pagination import LimitOffsetPagination

from images.decorators import (
    has_certain_thumbnail_size_permission,
    has_fetch_expiring_link_permission,
    has_use_original_image_link_permission,
    is_correct_user_for_original_image,
    is_correct_user_for_thumbnail,
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
    get_s3_client,
    get_s3_objects,
    get_temp_thumbnail_link,
    create_new_thumbnail,
    validate_thumbnail_size,
)
from website import settings


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
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


@api_view(["GET"])
@throttle_classes([OriginalImgLinkBurstThrottle, OriginalImgLinkSustainedThrottle])
@has_use_original_image_link_permission
@is_correct_user_for_original_image
def create_temp_original_image_link(request, img_name):
    """Creates a temporary link to the original version of the requested image."""
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
@is_correct_user_for_thumbnail
def create_temp_thumbnail_link(
    request, thumbnail_size, img_name, has_time_exp_permission
):
    """Creates a temporary link to a requested thumbnail size."""
    validation_status = validate_thumbnail_size(thumbnail_size)
    if validation_status != "Success":
        return validation_status

    time_exp = request.query_params.get("time_exp", None)
    if time_exp:
        if not has_time_exp_permission:
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        if not time_exp.isnumeric():
            return Response(
                {
                    "status": "Inappropriate argument type: time_exp has to be an integer"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if int(time_exp) < 300 or int(time_exp) > 30000:
            return Response(
                {
                    "status": "Inappropriate value: time_exp is not between 300 and 30000"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        time_exp = 120

    s3_client = get_s3_client()
    s3_objects = get_s3_objects(s3_client)

    img_path = f"images/{thumbnail_size}_{img_name}"
    file_exists_in_s3 = "Contents" in s3_objects and any(
        dictionary["Key"] == img_path for dictionary in s3_objects["Contents"]
    )
    if not file_exists_in_s3:
        create_new_thumbnail(thumbnail_size, img_name)
    temp_url = get_temp_thumbnail_link(s3_client, thumbnail_size, img_name, time_exp)
    return Response({"thumbnail_temporary_link": temp_url})
