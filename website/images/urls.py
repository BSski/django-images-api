from django.urls import include, path

from rest_framework.routers import DefaultRouter

from images.views import (
    create_temp_original_image_link,
    create_temp_thumbnail_link,
    home,
    ImageViewSet,
)


router = DefaultRouter()
router.register("images", ImageViewSet, basename="images")

app_name = "images"
urlpatterns = [
    path("home/", home, name="home"),
    path("", include(router.urls)),
    path(
        "thumbnails/<str:thumbnail_size>/<str:img_name>/",
        create_temp_thumbnail_link,
        name="create_temp_thumbnail_link",
    ),
    path(
        "original_picture/<str:img_name>/",
        create_temp_original_image_link,
        name="create_temp_original_image_link",
    ),
]
