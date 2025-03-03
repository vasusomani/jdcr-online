from django.contrib import admin
from solo.admin import SingletonModelAdmin

from core.models import *

# Register your models here.


class ArticleSectionStackedInline(admin.StackedInline):
    model = ArticleSection
    extra = 1
    classes = [
        "collapse",
    ]


class ArticleAuthorTabularInline(admin.TabularInline):
    model = ArticleAuthor
    extra = 1
    classes = [
        "collapse",
    ]


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = (
        "title",
        "article_type",
        "get_volume",
        "get_issue",
        "is_in_press",
    )  # "downloads", "views")
    search_fields = ("title",)
    list_per_page = 20
    list_filter = (
        "article_type",
        "published",
    )
    fieldsets = (
        (
            "Article",
            {
                "fields": (
                    "show_in_home",
                    "is_open_access",
                    "is_in_press",
                    "issue",
                    "url",
                    "article_type",
                    "title",
                    "doi",
                    "doi_link",
                    "pmid",
                    "pmid_link",
                    "abstract",
                    "page_from",
                    "page_to",
                    "keywords",
                    "how_to_cite",
                    "received",
                    "revised",
                    "accepted",
                    "published",
                    "available_on",
                    "downloads",
                    "views",
                    "pdf",
                    "xml",
                    "generate_xml",
                    "generate_pdf",
                )
            },
        ),
        ("Citations", {"fields": ("apa", "mla", "chicago", "harvard", "vancouver")}),
    )
    inlines = [ArticleSectionStackedInline, ArticleAuthorTabularInline]

    @admin.display(description="Volume")
    def get_volume(self, obj):
        return obj.issue.volume.name

    @admin.display(description="Issue")
    def get_issue(self, obj):
        return obj.issue.name


class EditorialBoardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "editor_type",
        "institution",
    )
    sortable_by = ("editor_type", "name")


class PolicyAdmin(admin.ModelAdmin):
    model = Policy
    readonly_fields = ("url",)


class SpecialIssueGuestEditorInlineAdmin(admin.TabularInline):
    model = SpecialIssueGuestEditor
    extra = 1
    classes = ("collapse",)


class IssueAdmin(admin.ModelAdmin):
    model = Issue
    list_display = (
        "name",
        "volume",
        "is_special_issue",
        "in_press",
    )
    fieldsets = (
        ("Standard Issue", {"fields": ("in_press", "volume", "name", "month")}),
        (
            "Special Issue",
            {
                "description": "Only fill up this form if this issue is a Special Issue",
                "fields": (
                    "is_special_issue",
                    "title",
                    "about",
                    "thumbnail",
                    "submission_deadline",
                    "is_published",
                    "published",
                ),
            },
        ),
    )
    inlines = [SpecialIssueGuestEditorInlineAdmin]


class ManuscriptSubmissionAdmin(admin.ModelAdmin):
    model = ManuscriptSubmission
    list_display = (
        "mrn",
        "title",
        "updated_at",
        "submitted_at",
    )
    fields = (
        "status",
        "payment_status",
        "user",
        "mrn",
        "email",
        "title",
        "abstract",
        "keywords",
        "article",
        "acceptance_letter",
        "invoice",
        "additional_file",
        "editorial_comment",
        "published_link",
        "send_reminder",
        "submitted_at",
        "updated_at",
    )
    readonly_fields = (
        "submitted_at",
        "updated_at",
    )


admin.site.register(User)
admin.site.register(Journal)
admin.site.register(Volume)
admin.site.register(Issue, IssueAdmin)
admin.site.register(News)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Announcement)
admin.site.register(ManuscriptSubmission, ManuscriptSubmissionAdmin)
admin.site.register(Indexing)
admin.site.register(FAQ)
admin.site.register(JournalRanking)
admin.site.register(EditorialBoard, EditorialBoardAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(PublicationFrequency, SingletonModelAdmin)
admin.site.register(ArticleProcessingCharges, SingletonModelAdmin)
admin.site.register(AdConfig, SingletonModelAdmin)
admin.site.register(SiteConfig, SingletonModelAdmin)
