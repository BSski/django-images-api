from .models import Image
from .serializers import ImageSerializer

# from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
import boto3
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from website import settings


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view()
def get_or_create_thumbnail_link(request, new_height, img_name):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    result = s3_client.list_objects_v2(
        Bucket=settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME
    )

    img_path = f"images/{new_height}_{img_name}"
    if "Contents" in result and any(
        dictionary["Key"] == img_path for dictionary in result["Contents"]
    ):
        print("Key exists in the bucket.")
    else:
        print("Key doesn't exist in the bucket. Adding a thumbnail.")
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        destination_bucket = settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME
        event_data = {
            "bucket_name": bucket_name,
            "destination_bucket_name": destination_bucket,
            "image_name": img_name,
            "new_height": new_height,
        }

        lambda_client = boto3.client("lambda", region_name="eu-central-1")
        lambda_response = lambda_client.invoke(
            FunctionName="CreateAndSaveThumbnailOnDemand",
            InvocationType="Event",
            Payload=json.dumps(event_data),
        )
    return Response({"URL": f"{new_height}/{img_name}"})

@api_view()
def get_or_create_thumbnail_link(request, new_height, img_name):
    # przekazuj tu request.params.get("temp_link") i jeśli jest, to dodatkowo
    # generuj temporary link do tego thumbnailsa
    # temp_link=300-30000, z tego zakresu liczba i to w sekundach po ilu expiruje

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    result = s3_client.list_objects_v2(
        Bucket=settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME
    )

    img_path = f"images/{new_height}_{img_name}"
    if "Contents" in result and any(
        dictionary["Key"] == img_path for dictionary in result["Contents"]
    ):
        print("Key exists in the bucket.")
    else:
        print("Key doesn't exist in the bucket. Adding a thumbnail.")
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        destination_bucket = settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME
        event_data = {
            "bucket_name": bucket_name,
            "destination_bucket_name": destination_bucket,
            "image_name": img_name,
            "new_height": new_height,
        }

        lambda_client = boto3.client("lambda", region_name="eu-central-1")
        lambda_response = lambda_client.invoke(
            FunctionName="CreateAndSaveThumbnailOnDemand",
            InvocationType="Event",
            Payload=json.dumps(event_data),
        )
    return Response({"URL": f"{new_height}/{img_name}"})


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
        ExpiresIn=30000
    )
    return Response({"original_image_temporary_link": temp_url})