from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url("admin", admin.site.urls),
    url("", include("wagtail_openedx.urls", namespace="wagtail_openedx")),
]
