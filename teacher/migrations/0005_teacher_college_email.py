# Generated by Django 5.1.1 on 2025-02-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_remove_teacher_modules_teacher_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='college_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
