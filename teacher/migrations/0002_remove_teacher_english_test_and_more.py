# Generated by Django 5.1.1 on 2024-09-27 07:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teacher", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacher",
            name="english_test",
        ),
        migrations.AlterField(
            model_name="teacher",
            name="date_joined",
            field=models.DateField(blank=True, null=True),
        ),
    ]
