from django.db import models
from solo.models import SingletonModel
from tinymce.models import HTMLField

from core.utils import dnb


class AdConfig(SingletonModel):
    ad_space_1 = models.ImageField(upload_to="ads", **dnb)
    ad_space_1_link = models.TextField(**dnb)
    ad_space_2 = models.ImageField(upload_to="ads", **dnb)
    ad_space_2_link = models.TextField(**dnb)
    ad_space_3 = models.ImageField(upload_to="ads", **dnb)
    ad_space_3_link = models.TextField(**dnb)
    responsive_ad_space_1 = models.ImageField(upload_to="ads", **dnb)
    responsive_ad_space_1_link = models.TextField(**dnb)
    responsive_ad_space_2 = models.ImageField(upload_to="ads", **dnb)
    responsive_ad_space_2_link = models.TextField(**dnb)

    def __str__(self):
        return "Ad Configuration"


class SiteConfig(SingletonModel):
    phone = models.CharField(max_length=32, **dnb)
    whatsapp = models.CharField(max_length=32, **dnb)
    submission_email = models.CharField(max_length=32, **dnb)
    support_email = models.CharField(max_length=32, **dnb)
    footer_copyright = models.CharField(max_length=255, **dnb)
    about_us = HTMLField(**dnb)
    contact_us = HTMLField(**dnb)
    privacy_policy = HTMLField(**dnb)
    terms_and_conditions = HTMLField(**dnb)
    copyright = HTMLField(**dnb)
    cookie_preference = HTMLField(**dnb)

    def __str__(self):
        return "Site Configuration"

class JournalRanking(models.Model):
    image = models.ImageField(upload_to="journal_rankings")
    link = models.TextField(**dnb)
    