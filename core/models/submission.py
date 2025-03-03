import mimetypes

from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.dispatch import receiver

from .user import User 
from .core import Journal
from core.template_builder import EmailTemplateBuilder

HOST = "jdcronline.org"

# article submission statuses
SUBMISSION_STATUS = (
    ("ACKNOWLEDGED", "ACKNOWLEDGED"),
    ("IN_REVIEW", "IN_REVIEW"),
    ("REVISION", "REVISION"),
    ("ACCEPTED", "ACCEPTED"),
    ("REJECTED", "REJECTED"),
    ("PUBLISHED", "PUBLISHED"),
)

PAYMENT_STATUS = (
    ("PENDING", "PENDING"),
    ("RECEIVED", "RECEIVED"),
)


class ManuscriptSubmission(models.Model):
    status = models.CharField(
        _("Status"),
        max_length=64,
        choices=SUBMISSION_STATUS,
        default="ACKNOWLEDGED",
    )
    payment_status = models.CharField(
        _("Payment Status"),
        max_length=64,
        choices=PAYMENT_STATUS,
        default="PENDING",
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="submissions"
    )
    mrn = models.CharField(_("MRN"), max_length=256, null=True, blank=True)
    email = models.CharField(_("Email"), max_length=256)
    title = models.TextField(_("Manuscript Title"))
    abstract = models.TextField(_("Abstract"), null=True, blank=True)
    keywords = models.TextField(_("Keywords"), null=True, blank=True)
    additional_file = models.FileField(_("Additional File"), null=True, blank=True)
    article = models.FileField(_("File"), upload_to="manuscript_submissions/")
    acceptance_letter = models.FileField(
        _("Acceptance Letter"),
        upload_to="acceptance_letter",
        null=True,
        blank=True,
    )
    invoice = models.FileField(
        _("Invoice"),
        upload_to="invoices",
        null=True,
        blank=True,
    )
    editorial_comment = models.TextField(_("Editorial Comment"), null=True, blank=True)
    published_link = models.TextField(_("Published Link"), null=True, blank=True)
    submitted_at = models.DateTimeField(_("Submitted On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Updated On"), auto_now=True)
    send_reminder = models.BooleanField(default=False)
    send_acceptance_letter = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Article Submission"
        verbose_name_plural = "Article Submissions"

    def __str__(self):
        return f"{self.mrn}"
    
    def send_revision_request(self):
        journal = Journal.objects.all().first()
        subject = f"Manuscript Revision Request for MRN: {self.mrn} - {journal.name}"
        etb = EmailTemplateBuilder()
        etb.revision(self.user, journal, self, f"support@{HOST}")
        message = etb.template
        email_from = settings.EMAIL_SENDER
        recipient_list = [
            self.user.email,
        ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"
        email.send()
    
    def send_rejection_letter(self):
        journal = Journal.objects.all().first()
        subject = f"Manuscript Rejection Letter for MRN: {self.mrn} - {journal.name}"
        etb = EmailTemplateBuilder()
        etb.rejection(self.user, journal, self, f"support@{HOST}")
        message = etb.template
        email_from = settings.EMAIL_SENDER
        recipient_list = [
            self.user.email,
        ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"
        email.send()
        
    def send_published_notification(self):
        journal = Journal.objects.all().first()
        subject = f"Manuscript Published Notification for MRN: {self.mrn} - {journal.name}"
        etb = EmailTemplateBuilder()
        etb.published(self.user, journal, self, f"support@{HOST}")
        message = etb.template
        email_from = settings.EMAIL_SENDER
        recipient_list = [
            self.user.email,
        ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"
        email.send()

    def send_payment_reminder(self):
        journal = Journal.objects.all().first()
        subject = f"APC Payment Reminder for MRN: {self.mrn} - {journal.name}"
        payment_link = f"https://{HOST}/payments/"
        etb = EmailTemplateBuilder()
        etb.reminder(self.user, journal, self, f"support@{HOST}", payment_link)
        message = etb.template
        email_from = settings.EMAIL_SENDER
        recipient_list = [
            self.user.email,
        ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"
        email.send()
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            # This is a new object, no previous status
            super().save(*args, **kwargs)
        else:
            # Existing object, check for status change
            old_self = ManuscriptSubmission.objects.get(pk=self.pk)
            if old_self.status != self.status:
                if self.status == "ACCEPTED":
                    self.send_acceptance_letter = True
                if self.status == "REJECTED":
                    self.send_rejection_letter()
                if self.status == "PUBLISHED":
                    self.send_published_notification()
                if self.status == "REVISION":
                    self.send_revision_request()
            
            if self.send_reminder:
                self.send_payment_reminder()
                self.send_reminder = False
            return super().save(*args, **kwargs)



@receiver(post_save, sender=ManuscriptSubmission)
def handle_post_save(sender, instance: ManuscriptSubmission, created, **kwargs):
    if instance.send_acceptance_letter:
        post_save.disconnect(handle_post_save, sender=sender)
        journal = Journal.objects.all().first()
        subject = f"Manuscript Acceptance Letter for MRN: {instance.mrn} - {journal.name}"
        etb = EmailTemplateBuilder()
        etb.acceptance(instance.user, journal, instance, f"support@{HOST}")
        message = etb.template
        email_from = settings.EMAIL_SENDER
        recipient_list = [
            instance.user.email,
        ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"

        # Attach files
        if instance.invoice and instance.invoice.name:
            with default_storage.open(instance.invoice.name) as invoice_file:
                mime_type, _ = mimetypes.guess_type(instance.invoice.name)
                filename = instance.invoice.name.split("/")[-1]
                email.attach(
                    filename=filename,
                    content=invoice_file.read(),
                    mimetype=mime_type or "application/pdf",
                )

        if instance.acceptance_letter and instance.acceptance_letter.name:
            with default_storage.open(
                instance.acceptance_letter.name
            ) as acceptance_letter_file:
                mime_type, _ = mimetypes.guess_type(instance.acceptance_letter.name)
                filename = instance.acceptance_letter.name.split("/")[-1]
                email.attach(
                    filename=filename,
                    content=acceptance_letter_file.read(),
                    mimetype=mime_type or "application/pdf",
                )

        email.send()
        
        instance.send_acceptance_letter = False
        instance.save()
    post_save.connect(handle_post_save, sender=ManuscriptSubmission)