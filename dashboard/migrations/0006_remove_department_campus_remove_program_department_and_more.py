# Generated by Django 5.1.1 on 2024-09-12 08:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_alter_program_campus"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="department",
            name="campus",
        ),
        migrations.RemoveField(
            model_name="program",
            name="department",
        ),
        migrations.AddField(
            model_name="department",
            name="campus",
            field=models.ManyToManyField(to="dashboard.campus"),
        ),
        migrations.AddField(
            model_name="program",
            name="department",
            field=models.ManyToManyField(to="dashboard.department"),
        ),
    ]
