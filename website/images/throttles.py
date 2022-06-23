from rest_framework import throttling


class AnonymousBurstThrottle(throttling.AnonRateThrottle):
    scope = 'anonymous_burst_throttle'


class AnonymousSustainedThrottle(throttling.AnonRateThrottle):
    scope = 'anonymous_sustained_throttle'


class OriginalImgLinkBurstThrottle(throttling.UserRateThrottle):
    scope = 'original_img_link_burst_throttle'


class OriginalImgLinkSustainedThrottle(throttling.UserRateThrottle):
    scope = 'original_img_link_sustained_throttle'


class ThumbnailLinkBurstThrottle(throttling.UserRateThrottle):
    scope = 'thumbnail_link_burst_throttle'


class ThumbnailLinkSustainedThrottle(throttling.UserRateThrottle):
    scope = 'thumbnail_link_sustained_throttle'


class GetImagesUserBurstThrottle(throttling.UserRateThrottle):
    scope = 'get_images_user_burst_throttle'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class PostImageUserBurstThrottle(throttling.UserRateThrottle):
    scope = 'get_images_user_burst_throttle'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class GetImagesUserSustainedThrottle(throttling.UserRateThrottle):
    scope = 'get_images_user_sustained_throttle'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class PostImageUserSustainedThrottle(throttling.UserRateThrottle):
    scope = 'post_image_user_sustained_throttle'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)
