from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination


@api_view()
def home(request):
    return Response({"message": "Welcome!"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    

# {
#     'ResponseMetadata': {
#         'RequestId': '4bcbe58b-b0cc-47a5-a1d9-79eda1987e58',
#         'HTTPStatusCode': 202,
#         'HTTPHeaders': {
#             'date': 'Tue, 21 Jun 2022 20:49:37 GMT',
#             'content-length': '0',
#             'connection': 'keep-alive',
#             'x-amzn-requestid': '4bcbe58b-b0cc-47a5-a1d9-79eda1987e58',
#             'x-amzn-remapped-content-length': '0',
#             'x-amzn-trace-id': 'root=1-62b22ee0-001eff650f0743dc798590f1;sampled=0'
#         },
#         'RetryAttempts': 0
#     },
#     'StatusCode': 202,
#     'Payload': <botocore.response.StreamingBody object at 0x000001DB413DB010>
# }

# {
#     'ResponseMetadata': {
#         'RequestId': 'P1BKB5DJ4G1WWRHC',
#         'HostId': 'ParLr2NhCWOHPkJhooS34e9t3E3w8nK6TdinklZfg+1r57qlgS+/MMRHxWFAn9OYEtzPpLg2L98=',
#         'HTTPStatusCode': 200,
#         'HTTPHeaders': {
#            'x-amz-id-2': 'ParLr2NhCWOHPkJhooS34e9t3E3w8nK6TdinklZfg+1r57qlgS+/MMRHxWFAn9OYEtzPpLg2L98=',
#             'x-amz-request-id': 'P1BKB5DJ4G1WWRHC',
#             'date': 'Tue, 21 Jun 2022 21:33:03 GMT',
#             'x-amz-bucket-region': 'eu-central-1',
#             'content-type': 'application/xml',
#             'transfer-encoding': 'chunked', 'server': 'AmazonS3'
#         },
#         'RetryAttempts': 1
#     },
#     'IsTruncated': False,
#     'Contents': [
#         {
#             'Key': 'images/',
#             'LastModified': datetime.datetime(2022, 6, 21, 20, 21, 45, tzinfo=tzutc()),
#             'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
#             'Size': 0,
#             'StorageClass': 'STANDARD'
#         },
#         {
#             'Key': 'images/ProceduraRozwiązaniProblemuInformatycznego.png',
#             'LastModified': datetime.datetime(2022, 6, 21, 20, 22, 24, tzinfo=tzutc()),
#             'ETag': '"40119faf0246909e11c6aaad29c7d124"',
#             'Size': 272693,
#             'StorageClass': 'STANDARD'
#         },
#         {
#             'Key': 'images/cat.png',
#             'LastModified': datetime.datetime(2022, 6, 21, 21, 2, 22, tzinfo=tzutc()),
#             'ETag': '"6c9ab03babfa733b5e2d114e4eeb252e"',
#             'Size': 477375,
#             'StorageClass': 'STANDARD'
#         }
#     ],
#     'Name': 'bsski-images-api',
#     'Prefix': '',
#     'MaxKeys': 1000,
#     'EncodingType': 'url',
#     'KeyCount': 3
# }
