# Generated by Django 5.1.1 on 2024-09-30 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notices',
            name='image',
        ),
    ]
