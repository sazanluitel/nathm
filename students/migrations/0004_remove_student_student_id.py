# Generated by Django 5.1.1 on 2024-09-18 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_college_email_student_team_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_id',
        ),
    ]
