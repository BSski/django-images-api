from rest_framework import throttling


class GetAnononymousThrottle(throttling.AnonRateThrottle):
    scope = 'get_anonymous_throttle'

class OriginalImgLinkBurstThrottle(throttling.UserRateThrottle):
    scope = 'original_img_link_burst_throttle'

class OriginalImgLinkSustainedThrottle(throttling.UserRateThrottle):
    scope = 'original_img_link_sustained_throttle'

class ThumbnailLinkBurstThrottle(throttling.UserRateThrottle):
    scope = 'thumbnail_link_burst_throttle'

class ThumbnailLinkSustainedThrottle(throttling.UserRateThrottle):
    scope = 'thumbnail_link_sustained_throttle'


#throttle uploading images
