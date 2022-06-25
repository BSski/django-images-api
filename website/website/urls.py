"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView


ADMIN_LOGIN_URL = os.environ.get("ADMIN_LOGIN_URL", "/hidden_admin_url")

urlpatterns = [
    path(f"{ADMIN_LOGIN_URL}/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("images/", include("images.urls")),
    path("users/", include("users.urls"), name="users"),
    path("", RedirectView.as_view(url="images/home", permanent=False), name="index"),
    # path('images/', include(('images.urls', 'images'), namespace="img")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
