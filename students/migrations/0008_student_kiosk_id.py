# Generated by Django 5.1.1 on 2024-09-21 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_remove_student_personal_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='kiosk_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
