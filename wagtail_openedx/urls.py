from django.conf.urls import url

from . import views

app_name = "wagtail_openedx"
urlpatterns = [
    url("sync-courses", views.sync_courses),
]
