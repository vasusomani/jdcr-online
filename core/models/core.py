from urllib.parse import quote_plus
from django.db import models
from core.utils import dnb
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Journal(models.Model):
    name = models.CharField(_("Journal Name"), max_length=256)
    abbreviation = models.CharField(_("Abbreviation Name"), max_length=256)
    subjects = models.TextField(_("Subjects (comma separated)"), **dnb)
    url = models.CharField(_("URL"), max_length=256)
    issn_print = models.CharField(_("ISSN Print"), max_length=256, **dnb)
    issn_online = models.CharField(_("ISSN Online"), max_length=256, **dnb)
    email = models.CharField(_("Email"), max_length=256, null=True, blank=True)
    thumbnail = models.ImageField(_("Thumbnail"), upload_to="journal_thumbnails")
    about = HTMLField(**dnb)
    aim_and_scope = HTMLField(**dnb)
    apc = models.CharField(_("Processing Charges"), max_length=256, **dnb)
    cite_score = models.FloatField(default=0.0)
    cite_score_link = models.CharField(max_length=256, **dnb)
    impact_factor = models.FloatField(default=0.0)
    impact_factor_link = models.CharField(max_length=256, **dnb)
    acceptance_rate = models.CharField(_("Acceptance Rate"), max_length=50)
    first_decision = models.CharField(
        _("Time to First Decision (in days)"), max_length=50, **dnb
    )
    acceptance_to_publication = models.CharField(
        _("Acceptance to publication (in days)"), max_length=50, **dnb
    )
    review_time = models.CharField(_("Review Time"), max_length=50, **dnb)
    logo = models.ImageField(**dnb)

    def save(self, *args, **kwargs):
        if not self.pk and Journal.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError("There is can be only one Journal")
        return super(Journal, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class Indexing(models.Model):
    name = models.TextField(**dnb)
    link = models.TextField(**dnb)
    image = models.ImageField(**dnb)
    show_in_home_page = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"


EDITOR_TYPES = (
    ("editor_in_chief", "Editor-In-Chief"),
    ("managing_editor", "Managing Editor"),
    ("associate_editor", "Associate Editor"),
    ("editorial_board_member", "Editorial Board Member"),
    ("advisory_board_member", "Advisory Board Member"),
)


class EditorialBoard(models.Model):
    editor_type = models.CharField(
        max_length=32, choices=EDITOR_TYPES, default="editorial_board_member"
    )
    name = models.CharField(max_length=256)
    qualification = models.TextField(**dnb)
    designation = models.TextField(**dnb)
    institution = models.TextField(**dnb)
    image = models.ImageField(upload_to="editors", **dnb)
    
    def __str__(self):
        return self.name
