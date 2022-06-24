import functools

from rest_framework import status
from rest_framework.response import Response


def is_correct_user_for_thumbnail(func):
    """Check whether the requesting user is the one who the image belongs to."""

    @functools.wraps(func)
    def wrapper_is_correct_user(
        request, thumbnail_size, img_name, has_time_exp_permission, *args, **kwargs
    ):
        if request.user.id != int(img_name.split("_")[0]):
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return func(
            request, thumbnail_size, img_name, has_time_exp_permission, *args, **kwargs
        )

    return wrapper_is_correct_user


def is_correct_user_for_original_image(func):
    """Check whether the requesting user is the one who the image belongs to."""

    @functools.wraps(func)
    def wrapper_is_correct_user(request, img_name, *args, **kwargs):
        if request.user.id != int(img_name.split("_")[0]):
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return func(request, img_name, *args, **kwargs)

    return wrapper_is_correct_user


def has_certain_thumbnail_size_permission(func):
    """
    Check whether the requesting user is permitted to get a link to a thumbnail of the
    requested size.
    """

    @functools.wraps(func)
    def wrapper_has_thumbnail_permission(request, thumbnail_size, *args, **kwargs):
        if int(thumbnail_size) not in request.user.user_tier.thumbnails_sizes["sizes"]:
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        func(request, thumbnail_size, *args, **kwargs)
        return func(request, thumbnail_size, *args, **kwargs)

    return wrapper_has_thumbnail_permission


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
        func(
            request, thumbnail_size, img_name, has_time_exp_permission, *args, **kwargs
        )
        return func(
            request, thumbnail_size, img_name, has_time_exp_permission, *args, **kwargs
        )

    return wrapper_has_fetch_expiring_link_permission


def has_use_original_image_link_permission(func):
    """
    Check whether the requesting user is permitted to get a link to the original image.
    """

    @functools.wraps(func)
    def wrapper_has_use_original_image_link_permission(request, *args, **kwargs):
        if not request.user.user_tier.can_use_original_image_link:
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return func(request, *args, **kwargs)

    return wrapper_has_use_original_image_link_permission
