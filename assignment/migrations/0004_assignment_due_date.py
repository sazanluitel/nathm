# Generated by Django 5.1.1 on 2024-10-03 12:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_remove_assignment_section_assignment_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
