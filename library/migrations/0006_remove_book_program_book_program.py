# Generated by Django 5.1.1 on 2024-10-04 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('library', '0005_library_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='program',
        ),
        migrations.AddField(
            model_name='book',
            name='program',
            field=models.ManyToManyField(to='dashboard.program'),
        ),
    ]
