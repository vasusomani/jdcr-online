from itertools import chain
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.db.models import Q, Func, Value, CharField, functions

from core.mixins import DataProviderMixin
from core.models import Article, EditorialBoard, News, Announcement, Indexing
from core.models.archives import ArticleAuthor
from core.models.misc import FAQ, ArticleProcessingCharges, Policy, PublicationFrequency
from core.models.config import SiteConfig, JournalRanking


class HomeView(DataProviderMixin, View):
    template_name = "core/home.html"

    def get(self, request):
        ctx = self.get_data()
        articles = Article.objects.filter(show_in_home=True)
        ctx.update(
            {
                "editor": EditorialBoard.objects.filter(
                    editor_type="editor_in_chief"
                ).first(),
                "latest_published": articles.filter(is_in_press=False).order_by(
                    "-published"
                )[:8],
                "most_downloaded": articles.filter(is_in_press=False).order_by(
                    "-downloads"
                )[:8],
                "most_popular": articles.filter(is_in_press=False).order_by("-views")[
                    :8
                ],
                "in_press": articles.filter(is_in_press=True)[:8],
                "news": News.objects.all().order_by("-created_on")[:2],
                "announcements": Announcement.objects.all().order_by("-created_on")[:2],
                "indexings": Indexing.objects.filter(show_in_home_page=True),
                "editor_in_chiefs": EditorialBoard.objects.filter(
                    editor_type="editor_in_chief"
                ),
                "journal_rankings": JournalRanking.objects.all()
            }
        )
        return render(request, self.template_name, ctx)


class AboutUsView(DataProviderMixin, View):
    template_name = "core/about-us.html"

    def get(self, request):
        ctx = self.get_data()
        ctx.update({"site_config": SiteConfig.get_solo()})
        return render(request, self.template_name, ctx)


class ContactUsView(DataProviderMixin, View):
    template_name = "core/contact-us.html"

    def get(self, request):
        ctx = self.get_data()
        ctx.update({"site_config": SiteConfig.get_solo()})
        return render(request, self.template_name, ctx)


class ErrorView(DataProviderMixin, View):
    template_name = "core/error.html"

    def get(self, request):
        ctx = self.get_data()
        return render(request, self.template_name, ctx)


class InsightsView(DataProviderMixin, View):
    template_name = "core/insights.html"

    def get(self, request):
        ctx = self.get_data()
        ctx["indexings"] = Indexing.objects.all().order_by("name")
        return render(request, self.template_name, ctx)


class FAQView(DataProviderMixin, TemplateView):
    template_name = "core/faq.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update({"faqs": FAQ.objects.all().order_by("question")})
        return render(request, self.template_name, ctx)


class SubmitArticleView(DataProviderMixin, TemplateView):
    template_name = "core/submit-article.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        return self.render_to_response(ctx)


class AboutView(DataProviderMixin, View):
    template_name = "about/about.html"
    about_type_map = {
        "aim-and-scope": "Aim & Scope",
        "editorial-board": "Editorial Board",
        "news": "News",
        "announcements": "Announcements",
    }

    def get(self, request, *args, **kwargs):
        about_type = kwargs.get("about_type")
        if about_type not in self.about_type_map.keys():
            return redirect("error")
        ctx = self.get_data()
        ctx["about_type"] = about_type
        ctx["about_type_label"] = self.about_type_map[about_type]

        if about_type == "editorial-board":
            editorial_board = EditorialBoard.objects.all()
            ctx["editor_in_chief"] = editorial_board.filter(
                editor_type="editor_in_chief"
            )
            ctx["associate_editor"] = editorial_board.filter(
                editor_type="associate_editor"
            )
            ctx["editorial_board_member"] = editorial_board.filter(
                editor_type="editorial_board_member"
            )
            ctx["advisory_board_member"] = editorial_board.filter(
                editor_type="advisory_board_member"
            )
            ctx["managing_editor"] = editorial_board.filter(
                editor_type="managing_editor"
            )
        elif about_type == "news":
            ctx["news"] = News.objects.all().order_by("-created_on")
        elif about_type == "announcements":
            ctx["announcements"] = Announcement.objects.all().order_by("-created_on")
            print(ctx["announcements"])
        return render(request, self.template_name, ctx)


class PolicyView(DataProviderMixin, TemplateView):
    template_name = "core/policy.html"

    def get(self, request, *args, **kwargs):
        policy_url = kwargs.get("url")
        ctx = self.get_data()
        try:
            ctx["policy"] = (
                Policy.objects.filter(url=policy_url).order_by("-id").first()
            )
        except Policy.DoesNotExist:
            ctx["policy"] = None
        return render(request, self.template_name, ctx)


class AuthorPublicationsView(DataProviderMixin, TemplateView):
    template_name = "search/author-publications.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        if request.GET.get("author"):
            author = ArticleAuthor.objects.filter(id=request.GET.get("author")).first()
            fullname = f"{author.first_name} {author.middle_name if author.middle_name else ''} {author.last_name}"
            # articles = Article.objects.filter(authors__fullname=fullname)
            articles = Article.objects.annotate(
                fullname=Func(
                    functions.Coalesce("authors__first_name", Value("")),
                    Value(" "),
                    functions.Coalesce("authors__middle_name", Value("")),
                    Value(" "),
                    functions.Coalesce("authors__last_name", Value("")),
                    function="CONCAT",
                    output_field=CharField(),
                )
            ).filter(fullname__icontains=fullname)
            ctx.update(
                {"author": author, "articles": articles, "count": articles.count()}
            )
        else:
            return redirect("error")
        return render(request, self.template_name, ctx)


class SearchView(DataProviderMixin, TemplateView):
    template_name = "search/results.html"

    def get(self, request, *args, **kwargs):
        results = None
        ctx = self.get_data()
        if request.GET.get("q"):
            query = request.GET.get("q")
            all_articles = Article.objects.filter(
                Q(title__icontains=query)
                | Q(abstract__icontains=query)
                | Q(keywords__icontains=query)
            )
            author_articles = Article.objects.filter(
                Q(authors__first_name__icontains=query)
                | Q(authors__middle_name__icontains=query)
                | Q(authors__last_name__icontains=query)
            )
            count = all_articles.count() + author_articles.count()
            articles = list(chain(all_articles, author_articles))
            ctx.update({"query": query, "articles": articles, "count": count})
        else:
            return redirect("error")

        return render(request, self.template_name, ctx)


class PublicationFrequencyView(DataProviderMixin, TemplateView):
    template_name = "core/publication-frequency.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        try:
            publication_freq = PublicationFrequency.objects.get()
        except:
            publication_freq = None
        ctx.update({"publication_freq": publication_freq})
        return self.render_to_response(ctx)


class APCView(DataProviderMixin, TemplateView):
    template_name = "core/apc.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        try:
            apc = ArticleProcessingCharges.objects.get()
        except:
            apc = None
        ctx.update({"apc": apc})
        return self.render_to_response(ctx)


class TermsAndConditionsView(DataProviderMixin, TemplateView):
    template_name = "core/terms-and-conditions.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update({"terms_and_conditions": SiteConfig.get_solo().terms_and_conditions})
        return render(request, self.template_name, ctx)


class PrivacyPolicyView(DataProviderMixin, TemplateView):
    template_name = "core/privacy-policy.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update({"privacy_policy": SiteConfig.get_solo().privacy_policy})
        return render(request, self.template_name, ctx)


class CopyrightView(DataProviderMixin, TemplateView):
    template_name = "core/copyright.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update({"copyright": SiteConfig.get_solo().copyright})
        return render(request, self.template_name, ctx)


class CookiePreferenceView(DataProviderMixin, TemplateView):
    template_name = "core/cookie-preference.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update({"cookie_preference": SiteConfig.get_solo().cookie_preference})
        return render(request, self.template_name, ctx)
