from django.urls import include, path
from rest_framework.routers import DefaultRouter
from images.views import (
    ImageViewSet,
    create_temp_thumbnail_link,
    create_temp_original_image_link,
)


router = DefaultRouter()
router.register("images", ImageViewSet, basename="images")

app_name = "images"
urlpatterns = [
    path("", include(router.urls)),
    path(
        "thumbnails/<str:new_height>/<str:img_name>/",
        create_temp_thumbnail_link,
        name="create_temp_thumbnail_link",
    ),
    path(
        "original_picture/<str:img_name>/",
        create_temp_original_image_link,
        name="create_temp_original_image_link",
    ),
]
