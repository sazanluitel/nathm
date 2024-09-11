# Generated by Django 5.1.1 on 2024-09-11 12:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('postcode', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EducationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_name', models.CharField(max_length=100)),
                ('institution_name', models.CharField(max_length=100)),
                ('graduation_year', models.IntegerField()),
                ('major_subject', models.CharField(max_length=100)),
                ('file', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('job_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(choices=[('TOEFL', 'TOEFL'), ('IELTS', 'IELTS'), ('PTE', 'PTE'), ('CAMBRIDGE', 'Cambridge'), ('OTHER', 'Other')], max_length=50)),
                ('score', models.FloatField(max_length=5)),
                ('date', models.DateField()),
                ('files', models.FileField(blank=True, null=True, upload_to='pdf/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('title', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(default='', max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('profile_image', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.addressinfo')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship_number', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=6)),
                ('date_of_birth_in_ad', models.DateField()),
                ('citizenship_img', models.TextField()),
                ('educational_history', models.ManyToManyField(to='userauth.educationhistory')),
                ('emergency_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.emergencycontact')),
                ('employment_history', models.ManyToManyField(to='userauth.employmenthistory')),
                ('english_test', models.ManyToManyField(to='userauth.englishtest')),
                ('permanent_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permanent_address', to='userauth.addressinfo')),
                ('temporary_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_address', to='userauth.addressinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
