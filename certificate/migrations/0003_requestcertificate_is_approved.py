# Generated by Django 5.1.1 on 2024-09-28 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "certificate",
            "0002_requestcertificate_file_requestcertificate_status_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="requestcertificate",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]
