# Generated by Django 5.1.1 on 2025-03-03 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0014_emergencycontact_user_alter_educationhistory_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
