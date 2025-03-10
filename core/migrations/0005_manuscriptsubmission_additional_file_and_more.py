# Generated by Django 4.2.5 on 2024-07-28 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_articleauthor_prefix_manuscriptsubmission_invoice_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="manuscriptsubmission",
            name="additional_file",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="Additional File"
            ),
        ),
        migrations.CreateModel(
            name="UserForgotPasswordToken",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="forgot_password_token",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
