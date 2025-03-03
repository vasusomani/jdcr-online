from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core.models.archives import Article, Issue
from core.models.misc import Policy


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # Add all your static URLs here
        return [
            ("home"),
            ("error"),
            ("search"),
            ("insights"),
            ("faq"),
            ("about", "aim-and-scope"),
            ("archives"),
            ("archive-latest-issue"),
            ("author-publications"),
        ]

    def location(self, item):
        if isinstance(item, tuple):
            view_name, *params = item
            return reverse(view_name, args=params)
        return reverse(item)


class ArticleSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return Article.objects.all()

    def location(self, item):
        return item.get_absolute_url()


class PolicySitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Policy.objects.all()

    def location(self, item):
        return item.get_absolute_url()
    
class ArchiveDetailsSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Issue.objects.all()

    def location(self, item):
        return item.get_absolute_url()
