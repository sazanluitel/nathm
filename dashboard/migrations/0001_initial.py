# Generated by Django 5.1.1 on 2024-09-06 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Campus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.IntegerField()),
                ("location", models.CharField(max_length=50)),
                ("contact", models.IntegerField()),
                ("image", models.ImageField(upload_to="Campus/")),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="Department/")),
                ("description", models.TextField()),
                (
                    "campus",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.campus",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("tenure", models.IntegerField(default=4)),
                (
                    "academic_plan",
                    models.CharField(
                        choices=[("year", "Year"), ("sem", "Semester")], max_length=20
                    ),
                ),
                ("image", models.ImageField(upload_to="Program/")),
                ("description", models.TextField()),
                (
                    "campus",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.campus",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Modules",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.IntegerField()),
                ("credit_hours", models.IntegerField()),
                ("level", models.IntegerField()),
                (
                    "program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.program",
                    ),
                ),
            ],
        ),
    ]
