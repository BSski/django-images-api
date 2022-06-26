import re

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible

import magic

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.response import Response


@deconstructible
class FileValidator(object):
    """
    Validator for images. Used for validating image maximum size and its content type.
    """

    error_messages = {
        "max_size": (
            "Ensure this file size is not greater than %(max_size)s."
            " Your file size is %(size)s."
        ),
        "min_size": (
            "Ensure this file size is not less than %(min_size)s. "
            "Your file size is %(size)s."
        ),
        "content_type": "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                "max_size": filesizeformat(self.max_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages["max_size"], "max_size", params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                "min_size": filesizeformat(self.min_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages["min_size"], "min_size", params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {"content_type": content_type}
                raise ValidationError(
                    self.error_messages["content_type"], "content_type", params
                )

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator)
            and self.max_size == other.max_size
            and self.min_size == other.min_size
            and self.content_types == other.content_types
        )


def validate_thumbnail_size_value(thumbnail_size):
    if not thumbnail_size or not thumbnail_size.isnumeric():
        return Response(
            {"status": "Inappropriate value: thumbnail size has to be an integer"},
            status=HTTP_400_BAD_REQUEST,
        )
    return "OK"


def validate_time_exp(time_exp):
    if not time_exp.isnumeric():
        return Response(
            {"status": "Inappropriate argument type: time_exp has to be an integer."},
            status=HTTP_400_BAD_REQUEST,
        )
    if int(time_exp) < 300 or int(time_exp) > 30000:
        return Response(
            {"status": "Inappropriate value: time_exp is not between 300 and 30000."},
            status=HTTP_400_BAD_REQUEST,
        )
    return "OK"


def validate_img_name(img_name):
    img_name_regex = re.compile(
        "(\d{0,8})_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.(jpe?g|png)"
    )
    if not re.fullmatch(img_name_regex, img_name):
        return Response(
            {"status": "Inappropriate value: image name is not valid."},
            status=HTTP_400_BAD_REQUEST,
        )
    return "OK"


def validate_if_correct_user(request, img_name):
    if request.user.id != int(img_name.split("_")[0]):
        return Response(
            {"status": "Forbidden: the user is not the owner of this image."},
            status=HTTP_403_FORBIDDEN,
        )
    return "OK"
