# Generated by Django 5.1.1 on 2024-09-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_alter_emergencycontact_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='relationship',
            field=models.CharField(blank=True, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Brother', 'Brother'), ('Relative', 'Relative'), ('OTHER', 'Other')], max_length=100, null=True),
        ),
    ]
