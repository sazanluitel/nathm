# Generated by Django 5.1.1 on 2025-04-24 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_modules_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='code',
            field=models.CharField(default='CODE1', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program',
            name='code',
            field=models.CharField(default='CODE2', max_length=20),
            preserve_default=False,
        ),
    ]
