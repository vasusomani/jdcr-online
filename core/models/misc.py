import re
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from tinymce.models import HTMLField

from core.utils import dnb
from core.models.user import User


def generate_choices(map):
    result = ()
    for k, v in map.items():
        result = result + ((k, v),)
    return result


class News(models.Model):
    heading = models.TextField(_("Heading"))
    content = HTMLField(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Announcement(models.Model):
    heading = models.TextField(_("Heading"))
    content = HTMLField(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"


# POLICY_MAP = {
#     "author-instruction": "Author Instruction",
#     "editorial-policies": "Editorial Policies",
#     "peer-review-process": "Peer Review Process",
#     "publication-ethics-policy": "Publication Ethics Policy",
#     "research-ethics-policy": "Research Ethics Policy",
#     "conflict-of-interest": "Conflict of Interest",
#     "open-access-statement": "Open Access Statement",
#     "content-licensing": "Content Licensing",
#     "copyright-and-permissions": "Copyright and Permissions",
#     "plagiarism-process": "Plagiarism Process",
#     "complaints-policy": "Complaints Policy",
#     "copyright-information": "Copyright Information",
# }


class Policy(models.Model):
    name = models.CharField(max_length=64, **dnb)
    url = models.CharField(max_length=64, **dnb)
    content = HTMLField()

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            super(Policy, self).save(*args, **kwargs)
        self.url = re.sub(r"(\W+)", "-", self.name, 0, re.IGNORECASE).lower()
        super(Policy, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("policy", kwargs={"url": self.url})
    
class FAQ(models.Model):
    question = models.TextField(**dnb)
    answer = HTMLField(**dnb)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class PublicationFrequency(SingletonModel):
    content = HTMLField(**dnb)

    def __str__(self):
        return "Publication Frequency"

    class Meta:
        verbose_name = "Publication Frequency"


class ArticleProcessingCharges(SingletonModel):
    content = HTMLField(**dnb)

    def __str__(self):
        return "Article Processing Charges"

    class Meta:
        verbose_name = "ArticleProcessingCharges"
