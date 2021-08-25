from django.db.utils import IntegrityError
from django.test import TestCase
from wagtail.core.models import Page

from .models import Category, CourseIndexPage, CoursePage


class CategoryTestCase(TestCase):
    def test_name_unique(self):
        name = "foo"
        Category.objects.create(name=name)
        with self.assertRaises(IntegrityError):
            Category.objects.create(name=name)


class CourseTestCase(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(pk=2)
        self.course_index = CourseIndexPage(title="Courses", slug="courses")
        self.root_page.add_child(instance=self.course_index)

    def test_title_parent(self):
        page = Page(title="foo")
        self.assertFalse(page.can_exist_under(self.course_index))
        course = CoursePage(title="bar")
        self.assertFalse(course.can_exist_under(self.root_page))
        self.assertTrue(course.can_exist_under(self.course_index))
