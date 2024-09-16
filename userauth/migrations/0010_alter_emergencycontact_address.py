# Generated by Django 5.1.1 on 2024-09-15 07:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0009_alter_personalinfo_educational_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userauth.addressinfo'),
        ),
    ]
