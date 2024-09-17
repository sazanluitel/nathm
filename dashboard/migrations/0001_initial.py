# Generated by Django 5.1.1 on 2024-09-17 05:50

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
                ("code", models.CharField(max_length=20)),
                ("location", models.CharField(max_length=50)),
                ("contact", models.CharField(max_length=15)),
                ("image", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
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
                ("image", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
                ("campus", models.ManyToManyField(to="dashboard.campus")),
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
                ("tenure", models.IntegerField(default=3)),
                (
                    "academic_plan",
                    models.CharField(
                        choices=[("year", "Year"), ("sem", "Semester")], max_length=20
                    ),
                ),
                ("image", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
                ("campus", models.ManyToManyField(to="dashboard.campus")),
                ("department", models.ManyToManyField(to="dashboard.department")),
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
                ("code", models.CharField(max_length=300)),
                ("credit_hours", models.IntegerField()),
                (
                    "level",
                    models.CharField(
                        choices=[("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")],
                        max_length=1,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("program", models.ManyToManyField(to="dashboard.program")),
            ],
        ),
    ]
