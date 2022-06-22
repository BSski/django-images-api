from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ImageViewSet,
    get_or_create_thumbnail_link,
    create_temporary_original_image_link
)


router = DefaultRouter()
router.register("images", ImageViewSet, basename="images")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "thumbnails/<str:new_height>/<str:img_name>/",
        get_or_create_thumbnail_link,
        name="get_or_create_thumbnail_link",
    ),
    path(
        "original_picture/<str:img_name>/",
        create_temporary_original_image_link,
        name="create_temporary_original_image_link"
    )
]
