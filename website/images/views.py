from .models import Image
from .serializers import ImageSerializer

# from rest_framework import permissions
from rest_framework import viewsets
import boto3
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from website import settings
from django.core.exceptions import ValidationError



class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view()
def create_temp_thumbnail_link(request, new_height, img_name):
    time_exp = request.GET.get("time_exp", None)
    if time_exp:
        if not time_exp.isnumeric():
            raise ValidationError(
                'Inappropriate argument type: time_exp has to be an integer'
            )
        if int(time_exp) < 300 or int(time_exp) > 30000:
            raise ValidationError(
                'Inappropriate value: time_exp is not between 300 and 30000'
            )
    else:
        time_exp = 300


    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    temp_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME,
            'Key': f'images/{new_height}_{img_name}',
        },
        ExpiresIn=time_exp
    )

    result = s3_client.list_objects_v2(
        Bucket=settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME
    )
    img_path = f"images/{new_height}_{img_name}"
    if "Contents" not in result or all(dictionary["Key"] != img_path for dictionary in result["Contents"]):
        print("Key doesn't exist in the bucket. Adding a thumbnail.")
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        destination_bucket = settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME

        ext = img_name.split('.')[-1]
        event_data = {
            "bucket_name": bucket_name,
            "destination_bucket_name": destination_bucket,
            "image_name": img_name,
            "new_height": new_height,
            "content_type": 'image/png' if ext == 'png' else 'image/jpeg'
        }
        lambda_client = boto3.client("lambda", region_name="eu-central-1")
        lambda_client.invoke(
            FunctionName="CreateAndSaveThumbnailOnDemand",
            InvocationType="Event",
            Payload=json.dumps(event_data),
        )

    return Response({"thumbnail_temporary_link": temp_url})


@api_view()
def create_temporary_original_image_link(request, img_name):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    temp_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': f'images/{img_name}',
        },
        ExpiresIn=1800
    )
    return Response({"original_image_temporary_link": temp_url})