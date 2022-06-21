from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, get_or_create_thumbnail_link


router = DefaultRouter()
router.register("images", ImageViewSet, basename="images")


urlpatterns = [
    path("", include(router.urls)),
    path("<str:owner_name>/<str:img_name>/<str:new_height>/", get_or_create_thumbnail_link, name='get_or_create_thumbnail_link'),
]
