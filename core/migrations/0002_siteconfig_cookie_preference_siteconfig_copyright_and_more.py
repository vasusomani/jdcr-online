# Generated by Django 4.2.5 on 2024-05-18 18:19

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfig",
            name="cookie_preference",
            field=tinymce.models.HTMLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="siteconfig",
            name="copyright",
            field=tinymce.models.HTMLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="siteconfig",
            name="privacy_policy",
            field=tinymce.models.HTMLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="siteconfig",
            name="terms_and_conditions",
            field=tinymce.models.HTMLField(blank=True, default=None, null=True),
        ),
    ]
