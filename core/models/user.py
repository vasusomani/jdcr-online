from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from core.utils import dnb
from tinymce.models import HTMLField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, **dnb)
    last_name = models.CharField(max_length=256, **dnb)
    photo = models.ImageField(upload_to="profile_photo/", null=True, blank=True)
    designation = models.TextField(**dnb)
    institution = models.TextField(**dnb)
    achievements = HTMLField(**dnb)
    publications = HTMLField(**dnb)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class UserEmailVerification(models.Model):
    user = models.ForeignKey(
        User, related_name="email_verifications", on_delete=models.CASCADE
    )
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserForgotPasswordToken(models.Model):
    user = models.ForeignKey(
        User, related_name="forgot_password_token", on_delete=models.CASCADE
    )
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
