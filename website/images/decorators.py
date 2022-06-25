import functools

from rest_framework import status
from rest_framework.response import Response

from images.validators import validate_thumbnail_size_value


def has_fetch_expiring_link_permission(func):
    """
    Check whether the requesting user is permitted to get a custom expiration time link
    to a thumbnail.
    """

    @functools.wraps(func)
    def wrapper_has_fetch_expiring_link_permission(
        request, thumbnail_size, img_name, *args, **kwargs
    ):
        has_time_exp_permission = bool(request.user.user_tier.can_fetch_expiring_link)
        return func(
            request, thumbnail_size, img_name, has_time_exp_permission, *args, **kwargs
        )

    return wrapper_has_fetch_expiring_link_permission


def has_certain_thumbnail_size_permission(func):
    """
    Check whether the requesting user is permitted to get a link to a thumbnail of the
    requested size. Validates `thumbnail_size` beforehand.
    """

    @functools.wraps(func)
    def wrapper_has_thumbnail_permission(request, thumbnail_size, *args, **kwargs):
        if (
            thumbnail_size_status := validate_thumbnail_size_value(thumbnail_size)
        ) != "OK":
            return thumbnail_size_status

        if int(thumbnail_size) not in request.user.user_tier.thumbnails_sizes["sizes"]:
            return Response(
                {
                    "status": "Forbidden: the user is not permitted to access this thumbnail size."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return func(request, thumbnail_size, *args, **kwargs)

    return wrapper_has_thumbnail_permission


def has_use_original_image_link_permission(func):
    """
    Check whether the requesting user is permitted to get a link to the original image.
    """

    @functools.wraps(func)
    def wrapper_has_use_original_image_link_permission(request, *args, **kwargs):
        if not request.user.user_tier.can_use_original_image_link:
            return Response(
                {
                    "status": "Forbidden: the user is not permitted to access original image link."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return func(request, *args, **kwargs)

    return wrapper_has_use_original_image_link_permission
