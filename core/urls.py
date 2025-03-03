from django.urls import path, include
from core.views import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("error/", ErrorView.as_view(), name="error"),
    path("about-us/", AboutUsView.as_view(), name="about-us"),
    path("contact-us/", ContactUsView.as_view(), name="contact-us"),
    path("search", SearchView.as_view(), name="search"),
    path("insights/", InsightsView.as_view(), name="insights"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("terms-and-conditions/", TermsAndConditionsView.as_view(), name="terms-and-conditions"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("copyright/", CopyrightView.as_view(), name="copyright"),
    path("cookie-preference/", CookiePreferenceView.as_view(), name="cookie-preference"),
    path("about/<str:about_type>/", AboutView.as_view(), name="about"),
    path("submit-article/", SubmitArticleView.as_view(), name="submit-article"),
    path("article/download/xml/<int:article_id>/", ArticleXMLDownloadView.as_view(), name="article-xml-download"),
    path("article/download/pdf/<int:article_id>/", ArticlePDFDownloadView.as_view(), name="article-pdf-download"),
    path("article/download/", ArticleDownloadView.as_view(), name="article-download"),
    path("article/<str:url>/", ArticleView.as_view(), name="article"),
    path("archives/", ArchiveListView.as_view(), name="archives"),
    path("archives/latest-issue/", ArchiveLatestIssueView.as_view(), name="archive-latest-issue"),
    path("archives/<str:vol>/<str:issue>/", ArchiveDetailsView.as_view(), name="archive-details"),
    path("policy/<str:url>/", PolicyView.as_view(), name="policy"),
    path("publications", AuthorPublicationsView.as_view(), name="author-publications"),
    path("publication-frequency/", PublicationFrequencyView.as_view(), name="publication-frequency"),
    path("article-processing-charges/", APCView.as_view(), name="apc"),
    path("articles-in-press/", ArticlesInPressView.as_view(), name="articles-in-press"),
    
    # Special Issue
    path("special-issue/about/", SpecialIssueAbout.as_view(), name="special-issue-about"),
    path("special-issue/propose/", SpecialIssuePropose.as_view(), name="special-issue-propose"),
    path("special-issue/open/", SpecialIssueOpen.as_view(), name="special-issue-open"),
    path("special-issue/published/", SpecialIssuePublished.as_view(), name="special-issue-published"),
    path("special-issue/<str:vol>/<str:issue>/", SpecialIssueDetails.as_view(), name="special-issue-details"),

    
    # Payments
    path("payments/", PaymentView.as_view(), name="payments"),
    path("payments/callback/", PaymentCallbackView.as_view(), name="payments-callback"),
    path("payments/success/", PaymentSuccessView.as_view(), name="payments-success"),
    path("payments/failed/", PaymentFailedView.as_view(), name="payments-failed"),
    
        
    # Author panel
    path("author/login/", AuthorLogin.as_view(), name="author-login"),
    path("author/logout/", AuthorLogout.as_view(), name="author-logout"),
    path("author/register/", AuthorRegister.as_view(), name="author-register"),
    path("author/articles/", AuthorArticles.as_view(), name="author-articles"),
    path("author/articles/<str:mrn>/", AuthorArticleDetails.as_view(), name="author-article-details"),
    path("author/article-submission/", AuthorArticleSubmission.as_view(), name="author-article-submission"),
    path("author/change-password/", AuthorChangePasswordView.as_view(), name="author-change-password"),
    path("author/forgot-password-email/", AuthorForgotPasswordEmailView.as_view(), name="author-forgot-password-email"),
    path("resend-verification-email/", AuthorResendEmailVerification.as_view(), name="author-resend-verification-link"),
    path("verify", AuthorEmailVerification.as_view(), name="author-email-verification"),
    path("reset-password", AuthorResetPasswordView.as_view(), name="reset-password"),
]