# Generated by Django 5.1.1 on 2024-09-22 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0009_alter_sections_campus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sections',
            name='user',
        ),
    ]
