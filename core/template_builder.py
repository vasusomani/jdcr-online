from pathlib import Path
from datetime import datetime
from django.conf import settings

from core.models import Journal, User

BASE_DIR = Path(__file__).resolve().parent.parent
EMAIL_TEMP_DIR = BASE_DIR / "core" / "email_templates"


class EmailTemplateBuilder:
    def __init__(self):
        self.template = None
        self.year = datetime.now().year
        self.email_verification_template = EMAIL_TEMP_DIR / "email_verification.html"
        self.acknowledgement_letter = EMAIL_TEMP_DIR / "acknowledgement_letter.html"
        self.acceptance_letter = EMAIL_TEMP_DIR / "acceptance_letter.html"
        self.rejection_letter = EMAIL_TEMP_DIR / "rejection_letter.html"
        self.published_notification = EMAIL_TEMP_DIR / "published_notification.html"
        self.payment_reminder = EMAIL_TEMP_DIR / "payment_reminder.html"
        self.revision_request = EMAIL_TEMP_DIR / "revision_request.html"
        self.reset_password = EMAIL_TEMP_DIR / "reset_password.html"

    def email_verification(
        self, user: User, journal: Journal, support_email, verification_link
    ):

        with open(self.email_verification_template, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace(
            "{EMAIL_VERIFICATION_LINK}", verification_link
        )
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))

    def acknowledgement(
        self,
        user: User,
        journal: Journal,
        manuscript,
        support_email: str,
    ):

        with open(self.acknowledgement_letter, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{ARTICLE_TITLE}", manuscript.title)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{MRN_NUMBER}", manuscript.mrn)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))
        
    def acceptance(
        self,
        user: User,
        journal: Journal,
        manuscript,
        support_email: str,
    ):

        with open(self.acceptance_letter, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{ARTICLE_TITLE}", manuscript.title)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{MRN_NUMBER}", manuscript.mrn)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))
        
    def rejection(
        self,
        user: User,
        journal: Journal,
        manuscript,
        support_email: str,
    ):

        with open(self.rejection_letter, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{ARTICLE_TITLE}", manuscript.title)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{MRN_NUMBER}", manuscript.mrn)
        self.template = self.template.replace("{EDITORIAL_COMMENT}", manuscript.editorial_comment)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))
        
    def published(
        self,
        user: User,
        journal: Journal,
        manuscript,
        support_email: str,
    ):

        with open(self.published_notification, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{ARTICLE_TITLE}", manuscript.title)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{MRN_NUMBER}", manuscript.mrn)
        self.template = self.template.replace("{PUBLISHED_LINK}", manuscript.published_link)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))
    
    def reminder(
        self,
        user: User,
        journal: Journal,
        manuscript,
        support_email: str,
        payment_link: str,
    ):

        with open(self.payment_reminder, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{ARTICLE_TITLE}", manuscript.title)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{MRN_NUMBER}", manuscript.mrn)
        self.template = self.template.replace("{PAYMENT_LINK}", payment_link)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))
        
    def revision(
        self,
        user: User,
        journal: Journal,
        manuscript,
        support_email: str,
    ):

        with open(self.revision_request, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{ARTICLE_TITLE}", manuscript.title)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{MRN_NUMBER}", manuscript.mrn)
        self.template = self.template.replace("{EDITORIAL_COMMENT}", manuscript.editorial_comment)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))

    def forgot_password(
        self,
        user: User,
        journal: Journal,
        support_email: str,
        forgot_password_link: str
    ):
        with open(self.reset_password, "r") as t:
            self.template = t.read()

        self.template = self.template.replace("{USER_NAME}", user.first_name)
        self.template = self.template.replace("{JOURNAL_NAME}", journal.name)
        self.template = self.template.replace("{FORGOT_PASSWORD_LINK}", forgot_password_link)
        self.template = self.template.replace("{SUPPORT_EMAIL}", support_email)
        self.template = self.template.replace("{YEAR}", str(self.year))