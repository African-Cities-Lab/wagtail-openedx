from io import BytesIO

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.images import ImageFile
from django.shortcuts import render
from django.utils.translation import ngettext
from wagtail.images.models import Image

from . import utils
from .models import CourseIndexPage, CoursePage, CourseRun, CourseRunSyncMode


@staff_member_required
def sync_courses(request):
    courses_url = f"{settings.OPENEDX_API_URL}/courses/v1/courses"
    response = requests.get(courses_url)
    courses = response.json()["results"]

    for course_dict in courses:
        org, slug, run = utils.split_course_key(course_dict["id"])
        try:
            course_page = CoursePage.objects.get(slug=slug)
        except CoursePage.DoesNotExist:
            course_index_page = CourseIndexPage.objects.first()
            # wagtail image from url - https://gist.github.com/eyesee1/1ea8e1b90bfe632cd31f5a90afc0370c
            img_url = course_dict["media"]["image"]["raw"]
            img_response = requests.get(img_url)
            img_filename = img_url.split("/")[-1]
            img = Image(
                title=img_filename,
                file=ImageFile(
                    BytesIO(img_response.content),
                    name=img_filename,
                ),
            )
            img.save()
            course_page = CoursePage(
                title=course_dict["name"],
                slug=slug,
                short_description=course_dict["short_description"],
                video_uri=course_dict["media"]["course_video"]["uri"],
                image=img,
            )
            course_index_page.add_child(instance=course_page)
            course_page.save_revision().publish()

        course_run = CourseRun(
            sync_mode=CourseRunSyncMode.MANUAL,
            resource_link=course_dict["blocks_url"],
            start=course_dict["start"],
            end=course_dict["end"],
            enrollment_start=course_dict["enrollment_start"],
            enrollment_end=course_dict["enrollment_end"],
        )
        course_run.save()
        course_page.runs.add(course_run)
        course_page.save_revision().publish()

        num_courses = len(courses)
        messages.success(
            request,
            ngettext(
                "%(num_courses)d course has been successfully synchronized from %(openedx_url)s",
                "%(num_courses)d courses have been successfully synchronized from %(openedx_url)s",
                num_courses,
            )
            % {
                "num_courses": num_courses,
                "openedx_url": settings.OPENEDX_API_URL,
            },
        )

        return render(request, "wagtail_openedx/course_sync.html", {})
