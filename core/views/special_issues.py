
from django.shortcuts import render
from django.views.generic import TemplateView

from core.mixins import DataProviderMixin
from core.models import Issue, Volume, Article


class SpecialIssueAbout(DataProviderMixin, TemplateView):
    template_name = "archives/special-issue/about.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        return render(request, self.template_name, ctx)
    
class SpecialIssuePropose(DataProviderMixin, TemplateView):
    template_name = "archives/special-issue/propose.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        return render(request, self.template_name, ctx)
    
class SpecialIssueOpen(DataProviderMixin, TemplateView):
    template_name = "archives/special-issue/open.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        open_si = Issue.objects.filter(is_special_issue=True, is_published=False).order_by("-submission_deadline")
        ctx.update({
            "special_issues": open_si
        })
        return render(request, self.template_name, ctx)
    
class SpecialIssuePublished(DataProviderMixin, TemplateView):
    template_name = "archives/special-issue/published.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        published_si = Issue.objects.filter(is_special_issue=True, is_published=True).order_by("-published")
        ctx.update({
            "special_issues": published_si
        })
        return render(request, self.template_name, ctx)
    
class SpecialIssueDetails(DataProviderMixin, TemplateView):
        template_name = "archives/special-issue/details.html"
    
        def get(self, request, *args, **kwargs):
            ctx = self.get_data()
            issue = Issue.objects.get(id=kwargs.get("issue"))
            ctx.update({
                "articles": Article.objects.filter(issue=issue).order_by("-published"),
                "volume": issue.volume,
                "issue": issue
            })
            return render(request, self.template_name, ctx)
        