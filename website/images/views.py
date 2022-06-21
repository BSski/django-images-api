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
def get_or_create_thumbnail_link(request, owner_name, img_name, new_height):
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    result = s3_client.list_objects_v2(Bucket=settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME)

    img_path = f'images/{owner_name}_{new_height}_{img_name}'
    if (
        'Contents' in result
        and any(dictionary['Key'] == img_path for dictionary in result['Contents'])
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
            "image_info": {
                "owner": owner_name,
                "new_height": new_height
            }
        }

        lambda_client = boto3.client('lambda', region_name='eu-central-1')
        lambda_response = lambda_client.invoke(
            FunctionName="CreateAndSaveThumbnailOnDemand",
            InvocationType='Event',
            Payload=json.dumps(event_data)
        )
    return Response({"URL": f'{owner_name}/{img_name}/{new_height}'})