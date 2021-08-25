from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

COURSE_CODE_MAX_LENGTH = 100
DEFAULT_CHAR_FIELD_MAX_LENGTH = 255


class OrganizationIndexPage(Page):
    subpage_types = ["OrganizationPage"]


class OrganizationPage(Page):
    parent_page_types = ["OrganizationIndexPage"]
    code = models.CharField(max_length=COURSE_CODE_MAX_LENGTH, verbose_name=_("code"))
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("logo"),
    )
    description = RichTextField(verbose_name=_("description"))

    content_panels = Page.content_panels + [
        FieldPanel("code"),
        ImageChooserPanel("logo"),
        FieldPanel("description", classname="full"),
    ]


class PersonIndexPage(Page):
    subpage_types = ["PersonPage"]


class PersonPage(Page):
    parent_page_types = ["PersonIndexPage"]
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("person"),
    )
    organization = ParentalManyToManyField(
        "OrganizationPage", verbose_name=_("organization")
    )
    picture = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("picture"),
    )
    bio = RichTextField(verbose_name=_("short bio"))

    content_panels = Page.content_panels + [
        FieldPanel("person"),
        FieldPanel("organization"),
        ImageChooserPanel("picture"),
        FieldPanel("bio", classname="full"),
    ]


@register_snippet
class Category(TranslatableMixin, models.Model):
    name = models.CharField(
        max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH, unique=True, verbose_name=_("name")
    )
    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("category")
        verbose_name_plural = _("categories")


# TODO: class Program?


class CourseRunSyncMode(models.TextChoices):
    """Course run synchronization mode choices for the "sync_mode" field."""

    MANUAL = "manual", _("Manual")
    SYNC_TO_DRAFT = "sync_to_draft", _("Synchronization to draft page")
    SYNC_TO_PUBLIC = "sync_to_public", _("Synchronization to public page")


@register_snippet
class CourseRun(TranslatableMixin, models.Model):
    sync_mode = models.CharField(
        max_length=20,
        choices=CourseRunSyncMode.choices,
        default=CourseRunSyncMode.MANUAL,
    )
    resource_link = models.CharField(
        _("resource link"), max_length=200, blank=True, null=True
    )
    start = models.DateTimeField(_("course start"), blank=True, null=True)
    end = models.DateTimeField(_("course end"), blank=True, null=True)
    enrollment_start = models.DateTimeField(
        _("enrollment start"), blank=True, null=True
    )
    enrollment_end = models.DateTimeField(_("enrollment end"), blank=True, null=True)
    # languages = MultiSelectField(
    #     max_choices=50,
    #     max_length=255,  # MySQL does not allow max_length > 255
    #     # Language choices are made lazy so that we can override them in our tests.
    #     # When set directly, they are evaluated too early and can't be changed with the
    #     # "override_settings" utility.
    #     choices=lazy(lambda: ALL_LANGUAGES, tuple)(),
    #     help_text=_("The list of languages in which the course content is available."),
    # )

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("course run")
        verbose_name_plural = _("course runs")


class CourseIndexPage(Page):
    subpage_types = ["CoursePage"]


class CoursePage(Page):
    parent_page_types = ["CourseIndexPage"]
    # code = models.CharField(max_length=COURSE_CODE_MAX_LENGTH, verbose_name=_("code"))

    # name = models.CharField(
    #     max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH, verbose_name=_("name")
    # )

    short_description = RichTextField(
        verbose_name=_("short description"), blank=True, null=True
    )
    full_description = RichTextField(
        verbose_name=_("full description"), blank=True, null=True
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        verbose_name=_("image"),
        blank=True,
        null=True,
    )

    video_uri = models.URLField(verbose_name=_("video"), blank=True, null=True)

    categories = ParentalManyToManyField(
        "Category", verbose_name=_("categories"), blank=True
    )
    instructors = ParentalManyToManyField(
        "PersonPage", verbose_name=_("instructors"), blank=True
    )

    runs = ParentalManyToManyField(
        "CourseRun",
        related_name="runs",
        verbose_name=_("course runs"),
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("short_description", classname="full"),
        FieldPanel("full_description", classname="full"),
        ImageChooserPanel("image"),
        FieldPanel("video_uri"),
        FieldPanel("categories"),
        FieldPanel("instructors"),
        FieldPanel("runs"),
    ]
