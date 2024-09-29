# Generated by Django 5.1.1 on 2024-09-29 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0003_requestcertificate_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestcertificate',
            name='certificate_type',
            field=models.CharField(choices=[('character', 'Characher Certificate'), ('training', 'Training Certificate'), ('academic', 'Academic Certificate')], max_length=100),
        ),
    ]
