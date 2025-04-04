# Generated by Django 5.1.1 on 2025-02-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_student_payment_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='about_us',
            field=models.CharField(blank=True, choices=[('ADVERTISING', 'Advertising'), ('EVENT', 'Event'), ('FRIENDS', 'Friend/Family/Colleague'), ('INTERNET', 'Internet Search'), ('MEDIAS', 'Social Media'), ('NEWS', 'News'), ('ALUMNI', 'Alumni'), ('OTHER', 'Other')], default='FRIENDS', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='annual_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='college_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='members_in_family',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='payment_by',
            field=models.CharField(blank=True, choices=[('STUDENT', 'Student'), ('PARENT', 'Parent/Guardian'), ('COMPANY', 'Company'), ('OTHER', 'Government/International Agency')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='payment_due',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='why_us',
            field=models.CharField(blank=True, choices=[('REPUTATION', 'Good brand Reputation'), ('LOCATION', 'Location'), ('COURSE', 'Course/Mode/Flexibility'), ('VALUE', 'Value of Money'), ('OTHER', 'Other')], default='REPUTATION', max_length=20, null=True),
        ),
    ]
