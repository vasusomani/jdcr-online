import os
import uuid
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from core.mixins import DataProviderMixin
from core.models import ManuscriptSubmission, UserEmailVerification, Journal, User, UserForgotPasswordToken
from core.template_builder import EmailTemplateBuilder


class AuthorLogin(DataProviderMixin, TemplateView):
    template_name = "author_panel/login.html"

    def get(self, request):
        ctx = self.get_data()
        if request.user.is_authenticated:
            return redirect("author-articles")
        return render(request, self.template_name, ctx)

    def post(self, request):
        ctx = self.get_data()
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("author-articles")
        else:
            ctx.update(
                {
                    "username": email,
                    "password": password,
                }
            )
            messages.error(request, "Wrong Credentials")
            return render(request, self.template_name, ctx)


class AuthorRegister(DataProviderMixin, TemplateView):
    template_name = "author_panel/register.html"

    def get(self, request):
        ctx = self.get_data()
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        try:
            user_exists = get_user_model().objects.get(email=request.POST.get("email"))
            messages.error(request, "User with email already exists")
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                email=request.POST.get("email"),
                designation=request.POST.get("designation"),
                is_email_verified=False,
                is_superuser=False,
                is_staff=False,
                is_active=True,
            )
            user.set_password(request.POST.get("password"))
            user.save()
            token = str(uuid.uuid4())
            user_mail_verification = UserEmailVerification.objects.create(
                user=user,
                token=token,
            )
            user_mail_verification.save()
            verification_url = f"{request.scheme}://{request.get_host()}/verify?token={token}&userEmail={request.POST.get('email')}"
            journal = Journal.objects.all().first()
            subject = f"Welcome to {journal.name} - Verify Your Email to Begin Your Research Journey!"
            etb = EmailTemplateBuilder()
            etb.email_verification(
                user, journal, f"support@{request.get_host()}", verification_url
            )
            message = etb.template
            email_from = settings.EMAIL_SENDER
            recipient_list = [
                request.POST.get("email"),
            ]
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.content_subtype = "html"
            email.send()
            messages.info(
                request,
                "User created successfully, please verify using the link sent to your email",
            )
        ctx = {}
        return render(request, self.template_name, ctx)


class AuthorLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("author-login")


class AuthorArticles(DataProviderMixin, TemplateView):
    template_name = "author_panel/articles.html"

    def get(self, request):
        ctx = self.get_data()
        if not request.user.is_authenticated:
            return redirect("author-login")
        articles = ManuscriptSubmission.objects.filter(user=request.user).order_by(
            "-submitted_at"
        )
        ctx.update({"articles": articles})
        return render(request, self.template_name, ctx)


class AuthorArticleDetails(DataProviderMixin, TemplateView):
    template_name = "author_panel/article-details.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        if not request.user.is_authenticated:
            return redirect("author-login")
        try:
            article = ManuscriptSubmission.objects.get(mrn=kwargs.get("mrn"))
        except:
            article = None
        ctx.update({"article": article})
        return render(request, self.template_name, ctx)
    
    def post(self, request, *args, **kwargs):
        ctx = self.get_data()
        if not request.user.is_authenticated:
            return redirect("author-login")
        try:
            article = ManuscriptSubmission.objects.get(mrn=kwargs.get("mrn"))
            article.additional_file = request.FILES.get("additional_file")
            article.save()
        except:
            article = None
        ctx.update({"article": article})
        return self.render_to_response(ctx)
        


class AuthorArticleSubmission(DataProviderMixin, TemplateView):
    template_name = "author_panel/article-submission.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("author-login")
        ctx = self.get_data()
        return render(request, self.template_name, ctx)

    def post(self, request):
        ctx = self.get_data()
        try:
            manuscript = ManuscriptSubmission.objects.create(
                user=request.user,
                email=request.user.email,
                title=request.POST.get("title"),
                abstract=request.POST.get("abstract"),
                keywords=request.POST.get("keywords"),
                article=request.FILES.get("article"),
            )
            manuscript.save()
            manuscript.mrn = f"MRN-{str(manuscript.pk).zfill(7)}"
            manuscript.save()
            journal = Journal.objects.all().first()
            subject = (
                f"Acknowledgement Letter for MRN: {manuscript.mrn} - {journal.name}"
            )
            etb = EmailTemplateBuilder()
            etb.acknowledgement(
                user=request.user,
                journal=journal,
                manuscript=manuscript,
                support_email=f"support@{request.get_host()}",
            )
            message = etb.template
            email_from = settings.EMAIL_SENDER
            recipient_list = [
                request.user.email,
            ]
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.content_subtype = "html"
            email.send()
            messages.info(request, "Your article was submitted successfully")
            return redirect("author-article-submission")
        except:
            messages.error(request, "There was an error while submitting article")
            ...
        return render(request, self.template_name, ctx)


class AuthorResendEmailVerification(View):
    def get(self, request):
        # user_mail_verification = UserEmailVerification.objects.filter(
        #     user=user,
        # ).first()
        user_mail_verification = UserEmailVerification.objects.get(user=request.user)

        verification_url = f"{request.scheme}://{request.get_host()}/verify?token={user_mail_verification.token}&userEmail={request.user.email}"
        journal = Journal.objects.all().first()
        subject = f"Welcome to {journal.name} - Verify Your Email to Begin Your Research Journey!"
        etb = EmailTemplateBuilder()
        etb.email_verification(
            request.user, journal, f"support@{request.get_host()}", verification_url
        )
        message = etb.template
        email_from = settings.EMAIL_SENDER
        recipient_list = [
            request.user.email,
        ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"
        email.send()
        messages.info(request, "Verification Link Sent")
        return redirect("author-articles")


class AuthorEmailVerification(DataProviderMixin, View):

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        try:
            user = get_user_model().objects.get(email=request.GET.get("userEmail"))
            email_verification = UserEmailVerification.objects.get(
                user=user, token=request.GET.get("token")
            )
            user.is_email_verified = True
            user.save()
            email_verification.delete()
            messages.info(request, "Email verified successfully")
            if request.user.is_authenticated:
                return redirect("author-articles")
            else:
                return redirect("author-login")
        except:
            messages.error(request, "Email Verification Failed")
            return redirect("author-login")


class AuthorChangePasswordView(DataProviderMixin, TemplateView):
    template_name = "author_panel/change-password.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_data()
        user = request.user

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password2 = request.POST.get("new_password2")

        ctx["success"] = "false"

        if user.check_password(old_password):
            if new_password == new_password2:
                user.set_password(new_password)
                user.save()
                messages.success(
                    request,
                    "Password Changed Successfully. You'll be logged out now in 5 secs. Please login again.",
                )
                ctx["success"] = "true"
            else:
                messages.error(
                    request,
                    "Confirm password mismatch, please enter the new password and confirm it.",
                )
        else:
            messages.error(request, "Old password didn't match with our records")

        return self.render_to_response(ctx)


class AuthorForgotPasswordEmailView(DataProviderMixin, TemplateView):
    template_name = "author_panel/forgot-password-email.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_data()

        email = request.POST.get("email")

        try:
            user = get_user_model().objects.get(email=email)
            
            UserForgotPasswordToken.objects.filter(user=user).delete()
            
            token = str(uuid.uuid4())
            forgot_password_token = UserForgotPasswordToken.objects.create(
                user=user,
                token=token,
            )
            forgot_password_token.save()
            
            forgot_password_link = f"{request.scheme}://{request.get_host()}/reset-password?token={token}&userEmail={user.email}"
            
            etb = EmailTemplateBuilder()
            etb.forgot_password(
                user, ctx["journal"], f"support@{request.get_host()}", forgot_password_link
            )
            message = etb.template
            subject = f"Reset Your Password - {ctx['journal']}"
            email_from = settings.EMAIL_SENDER
            recipient_list = [
                user.email,
            ]
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.content_subtype = "html"
            email.send()
            
            
        except get_user_model().DoesNotExist:
            ...

        messages.info(
            request,
            "Thank you! If the email address you provided is associated with an account, you will receive a password reset link shortly. Please check your inbox (and spam folder) for further instructions.",
        )
        
        return self.render_to_response(ctx)

class AuthorResetPasswordView(DataProviderMixin, TemplateView):
    template_name = "author_panel/reset-password.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        try:
            user = User.objects.get(email=request.GET.get("userEmail"))
            forgot_password = UserForgotPasswordToken.objects.get(
                user=user, token=request.GET.get("token")
            )
            user.save()
            # forgot_password.delete()
            # UserForgotPasswordToken.objects.filter(user=user).delete()
            return self.render_to_response(ctx)
        except:
            messages.error(request, "Failed to verify Password Reset Link, please try again")
            return redirect("author-login")
        
    def post(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx["success"] = "false"
        
        new_password = request.POST.get("new_password")
        new_password2 = request.POST.get("new_password2")
        if new_password != new_password2:
            messages.error(request, "Password mismatch")
            return self.render_to_response(ctx)
        
        try:
            user = User.objects.get(email=request.GET.get("userEmail"))
            forgot_password = UserForgotPasswordToken.objects.get(
                user=user, token=request.GET.get("token")
            )
            forgot_password.delete()
            UserForgotPasswordToken.objects.filter(user=user).delete()
            user.set_password(new_password)
            user.save()
            ctx["success"] = "true"
            messages.info(request, "Your password has been reset successfully. You will be redirected to login page shortly, after which you may login with your new password")
        except:
            return redirect("author-login")
        return self.render_to_response(ctx)
        
    
    