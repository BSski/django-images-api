from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet


router = DefaultRouter()
router.register("images", ImageViewSet, basename="images")


urlpatterns = [
    url('', include(router.urls)),
]
