# Generated by Django 5.1.1 on 2024-10-04 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_remove_paymenthistory_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='payment_method',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
