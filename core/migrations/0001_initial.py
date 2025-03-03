# Generated by Django 4.2.5 on 2024-04-26 04:18

import core.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photo/')),
                ('designation', models.TextField(blank=True, default=None, null=True)),
                ('institution', models.TextField(blank=True, default=None, null=True)),
                ('achievements', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('publications', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', core.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_space_1', models.ImageField(blank=True, default=None, null=True, upload_to='ads')),
                ('ad_space_1_link', models.TextField(blank=True, default=None, null=True)),
                ('ad_space_2', models.ImageField(blank=True, default=None, null=True, upload_to='ads')),
                ('ad_space_2_link', models.TextField(blank=True, default=None, null=True)),
                ('ad_space_3', models.ImageField(blank=True, default=None, null=True, upload_to='ads')),
                ('ad_space_3_link', models.TextField(blank=True, default=None, null=True)),
                ('responsive_ad_space_1', models.ImageField(blank=True, default=None, null=True, upload_to='ads')),
                ('responsive_ad_space_1_link', models.TextField(blank=True, default=None, null=True)),
                ('responsive_ad_space_2', models.ImageField(blank=True, default=None, null=True, upload_to='ads')),
                ('responsive_ad_space_2_link', models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField(verbose_name='Heading')),
                ('content', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_in_home', models.BooleanField(default=True)),
                ('is_in_press', models.BooleanField(default=False)),
                ('url', models.TextField(blank=True, default=None, null=True)),
                ('article_type', models.CharField(choices=[('Research Article', 'Research Article'), ('Mini Review Article', 'Mini Review Article'), ('Commentary Article', 'Commentary Article'), ('Review Article', 'Review Article'), ('Short Communication', 'Short Communication'), ('Short Commentary Article', 'Short Commentary Article'), ('Case Report', 'Case Report'), ('Case Series', 'Case Series'), ('Clinical Images', 'Clinical Images'), ("Editor's pick", "Editor's pick"), ('Editorial', 'Editorial'), ('Elective Report', 'Elective Report'), ('Letter to the Editor', 'Letter to the Editor'), ('News Article', 'News Article'), ('News Section', 'News Section'), ('Original Article', 'Original Article'), ('Perspective Article', 'Perspective Article')], max_length=128, verbose_name='Article Type')),
                ('title', models.TextField(blank=True, default=None, null=True)),
                ('doi', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='DOI')),
                ('doi_link', models.TextField(blank=True, default=None, null=True, verbose_name='DOI Link')),
                ('pmid', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='PMID')),
                ('pmid_link', models.TextField(blank=True, default=None, null=True, verbose_name='PMID Link')),
                ('abstract', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('page_from', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('page_to', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('keywords', models.TextField(blank=True, default=None, null=True)),
                ('how_to_cite', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('received', models.DateField(blank=True, default=None, null=True)),
                ('revised', models.DateField(blank=True, default=None, null=True)),
                ('accepted', models.DateField(blank=True, default=None, null=True)),
                ('published', models.DateField(blank=True, default=None, null=True)),
                ('available_on', models.DateField(blank=True, default=None, null=True)),
                ('is_open_access', models.BooleanField(default=True)),
                ('downloads', models.PositiveBigIntegerField(default=0)),
                ('views', models.PositiveBigIntegerField(default=0)),
                ('apa', models.TextField(blank=True, default=None, null=True)),
                ('mla', models.TextField(blank=True, default=None, null=True)),
                ('chicago', models.TextField(blank=True, default=None, null=True)),
                ('vancouver', models.TextField(blank=True, default=None, null=True)),
                ('harvard', models.TextField(blank=True, default=None, null=True)),
                ('pdf', models.FileField(blank=True, default=None, null=True, upload_to='articles/pdfs')),
                ('xml', models.FileField(blank=True, default=None, null=True, upload_to='articles/xmls')),
                ('generate_xml', models.BooleanField(default=False)),
                ('generate_pdf', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleProcessingCharges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'ArticleProcessingCharges',
            },
        ),
        migrations.CreateModel(
            name='EditorialBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor_type', models.CharField(choices=[('editor_in_chief', 'Editor-In-Chief'), ('managing_editor', 'Managing Editor'), ('associate_editor', 'Associate Editor'), ('editorial_board_member', 'Editorial Board Member'), ('advisory_board_member', 'Advisory Board Member')], default='editorial_board_member', max_length=32)),
                ('name', models.CharField(max_length=256)),
                ('qualification', models.TextField(blank=True, default=None, null=True)),
                ('designation', models.TextField(blank=True, default=None, null=True)),
                ('institution', models.TextField(blank=True, default=None, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='editors')),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, default=None, null=True)),
                ('answer', tinymce.models.HTMLField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='Indexing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, default=None, null=True)),
                ('link', models.TextField(blank=True, default=None, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='')),
                ('show_in_home_page', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_press', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=32, verbose_name='Issue Name')),
                ('month', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='Month')),
                ('is_special_issue', models.BooleanField(default=False, verbose_name='This is a Special Issue')),
                ('title', models.TextField(blank=True, default=None, null=True, verbose_name='Special Issue Title')),
                ('about', tinymce.models.HTMLField(blank=True, default=None, null=True, verbose_name='Special Issue About')),
                ('thumbnail', models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='Special Issue Cover')),
                ('submission_deadline', models.DateField(blank=True, default=None, null=True, verbose_name='Special Issue Submission Deadline')),
                ('is_published', models.BooleanField(default=False, verbose_name='This Speical Issue is published?')),
                ('published', models.DateField(blank=True, default=None, null=True, verbose_name='Special Issue Published Date')),
            ],
            options={
                'ordering': [models.Func(models.F('volume__name'), function='LENGTH'), 'volume__name'],
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Journal Name')),
                ('abbreviation', models.CharField(max_length=256, verbose_name='Abbreviation Name')),
                ('subjects', models.TextField(blank=True, default=None, null=True, verbose_name='Subjects (comma separated)')),
                ('url', models.CharField(max_length=256, verbose_name='URL')),
                ('issn_print', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='ISSN Print')),
                ('issn_online', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='ISSN Online')),
                ('email', models.CharField(blank=True, max_length=256, null=True, verbose_name='Email')),
                ('thumbnail', models.ImageField(upload_to='journal_thumbnails', verbose_name='Thumbnail')),
                ('about', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('aim_and_scope', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('apc', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Processing Charges')),
                ('cite_score', models.FloatField(default=0.0)),
                ('impact_factor', models.FloatField(default=0.0)),
                ('acceptance_rate', models.CharField(max_length=50, verbose_name='Acceptance Rate')),
                ('first_decision', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Time to First Decision (in days)')),
                ('acceptance_to_publication', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Acceptance to publication (in days)')),
                ('review_time', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Review Time')),
                ('logo', models.ImageField(blank=True, default=None, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField(verbose_name='Heading')),
                ('content', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('email', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, default=None, max_length=31, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=31, null=True)),
                ('amount', models.PositiveBigIntegerField(blank=True, default=None, null=True)),
                ('currency', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('remarks', models.TextField(blank=True, default=None, null=True)),
                ('rzp_order_id', models.CharField(max_length=255)),
                ('rzp_payment_id', models.CharField(max_length=255)),
                ('rzp_signature', models.CharField(max_length=255)),
                ('payment_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('url', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('content', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name': 'Policy',
                'verbose_name_plural': 'Policies',
            },
        ),
        migrations.CreateModel(
            name='PublicationFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'Publication Frequency',
            },
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_us', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('contact_us', tinymce.models.HTMLField(blank=True, default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_press', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=32, verbose_name='Volume Name')),
                ('year', models.CharField(max_length=32, verbose_name='Year')),
            ],
            options={
                'ordering': [models.Func(models.F('name'), function='LENGTH'), 'name'],
            },
        ),
        migrations.CreateModel(
            name='UserEmailVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_verifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialIssueGuestEditor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Full Name')),
                ('email', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('orcid_id', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('affiliation', models.TextField(blank=True, default=None, null=True, verbose_name='Affilication')),
                ('qualification', models.TextField(blank=True, default=None, null=True, verbose_name='Qualification')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_editors', to='core.issue')),
            ],
        ),
        migrations.CreateModel(
            name='ManuscriptSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ACKNOWLEDGED', 'ACKNOWLEDGED'), ('IN_REVIEW', 'IN_REVIEW'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('PUBLISHED', 'PUBLISHED')], default='ACKNOWLEDGED', max_length=64, verbose_name='Status')),
                ('payment_status', models.CharField(choices=[('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED')], default='PENDING', max_length=64, verbose_name='Payment Status')),
                ('mrn', models.CharField(blank=True, max_length=256, null=True, verbose_name='MRN')),
                ('email', models.CharField(max_length=256, verbose_name='Email')),
                ('title', models.TextField(verbose_name='Manuscript Title')),
                ('abstract', models.TextField(blank=True, null=True, verbose_name='Abstract')),
                ('keywords', models.TextField(blank=True, null=True, verbose_name='Keywords')),
                ('article', models.FileField(upload_to='manuscript_submissions/', verbose_name='File')),
                ('acceptance_letter', models.FileField(blank=True, null=True, upload_to='acceptance_letter', verbose_name='Acceptance Letter')),
                ('editorial_comment', models.TextField(blank=True, null=True, verbose_name='Editorial Comment')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='Submitted On')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Article Submission',
                'verbose_name_plural': 'Article Submissions',
            },
        ),
        migrations.AddField(
            model_name='issue',
            name='volume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='core.volume'),
        ),
        migrations.CreateModel(
            name='ArticleSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('content', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='core.article')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Last Name')),
                ('email', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('orcid_id', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('affiliation', models.TextField(blank=True, default=None, null=True, verbose_name='Affilication')),
                ('qualification', models.TextField(blank=True, default=None, null=True, verbose_name='Qualification')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='core.article')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='core.issue'),
        ),
    ]
