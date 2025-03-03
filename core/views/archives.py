import mimetypes
import os
import re
import requests
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View, CreateView

from core.mixins import DataProviderMixin
from core.models import Article, EditorialBoard, News, Announcement, Indexing
from core.models.archives import ArticleAuthor, ArticleSection, Issue, Volume


class ArchiveListView(DataProviderMixin, TemplateView):
    template_name = "archives/list.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx["volumes"] = Volume.objects.filter(in_press=False).order_by("-year")
        return render(request, self.template_name, ctx)


class ArchiveDetailsView(DataProviderMixin, TemplateView):
    template_name = "archives/details.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        try:
            issue = Issue.objects.get(id=kwargs.get("issue"))
            ctx["articles"] = Article.objects.filter(issue=issue).order_by("-page_from")
            ctx["volume"] = issue.volume
            ctx["issue"] = issue
        except:
            return redirect("error")
        return render(request, self.template_name, ctx)


class ArticlesInPressView(DataProviderMixin, TemplateView):
    template_name = "archives/in-press.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update({"articles": Article.objects.filter(is_in_press=True)})
        return render(request, self.template_name, ctx)


class ArticleView(DataProviderMixin, TemplateView):
    template_name = "archives/article.html"

    def split_keywords(self, article: Article):
        if article.keywords:
            split_list = re.split(r"(?<!^);|(?!^),", article.keywords)
            return [word.lstrip().rstrip() for word in split_list if word.strip()]
        else:
            return []

    def get(self, request, *args, **kwargs):
        try:
            ctx = self.get_data()
            article = Article.objects.get(url=kwargs.get("url"))
            article.views += 1
            article.save()
            if article.keywords:
                ctx["recommended"] = Article.objects.filter(
                    keywords__icontains=article.keywords
                ).exclude(id=article.id)[:5]
                if not ctx["recommended"]:
                    ctx["recommended"] = (
                        Article.objects.all()
                        .order_by("views")
                        .exclude(id=article.id)[:4]
                    )

            affiliations = {}
            aff_counter = 1
            for author in ArticleAuthor.objects.filter(article=article):
                if author.affiliation not in affiliations:
                    affiliations.update({author.affiliation: aff_counter})
                    aff_counter += 1
            authors = []
            for author in ArticleAuthor.objects.filter(article=article):
                temp = author.__dict__
                temp.update(
                    {
                        "full_name": author.full_name,
                        "author_affiliation_id": (
                            affiliations.get(author.affiliation)
                            if author.affiliation
                            else None
                        ),
                    }
                )
                authors.append(temp)
            ctx.update(
                {
                    "authors": authors,
                    "affiliations": affiliations,
                    "article": article,
                    "keywords": self.split_keywords(article),
                }
            )
        except Exception as e:
            print(e)
            return redirect("error")
        return render(request, self.template_name, ctx)


class ArchiveLatestIssueView(DataProviderMixin, View):
    def get(self, request, *args, **kwargs):
        latest_vol = Volume.objects.all().order_by("-id")[0]
        issue = Issue.objects.filter(volume=latest_vol).order_by("-id")[0]
        return redirect(
            reverse(
                "archive-details", kwargs={"vol": issue.volume.id, "issue": issue.id}
            )
        )


class ArticleDownloadView(View):

    def send_subscriber(self, request):
        IARCON_API_BASE = os.getenv("IARCON_API_BASE")
        url = f"{IARCON_API_BASE}/webapp/subscriber"
        data = {"email": request.POST.get("email"), "from": request.get_host()}
        AUTH_TOKEN = os.getenv("IARCON_TOKEN")
        headers = {"Authorization": AUTH_TOKEN, "Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get("article_id")))
        article.downloads += 1
        article.save()

        self.send_subscriber(request)

        if article.pdf:
            file_path = article.pdf.path

            filename = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)

            response = FileResponse(open(file_path, "rb"))
            response["Content-Type"] = mime_type or "application/pdf"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        else:
            return redirect(reverse("article", kwargs={"url": article.url}))


class ArticlePDFDownloadView(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(kwargs.get("article_id")))
        article.downloads += 1
        article.save()

        if article.pdf:
            file_path = article.pdf.path

            filename = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)

            response = FileResponse(open(file_path, "rb"))
            response["Content-Type"] = mime_type or "application/pdf"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        else:
            return redirect(reverse("article", kwargs={"url": article.url}))


class ArticleXMLDownloadView(View):

    def get(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=kwargs.get("article_id"))
            article.downloads += 1
            article.save()

            file_path = article.xml.path

            filename = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)

            response = FileResponse(open(file_path, "rb"))
            response["Content-Type"] = mime_type or "application/xml"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except:
            return redirect("error")
