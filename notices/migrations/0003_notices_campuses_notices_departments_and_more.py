# Generated by Django 5.1.1 on 2025-04-24 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_campus_code_alter_modules_code'),
        ('notices', '0002_remove_notices_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='notices',
            name='campuses',
            field=models.ManyToManyField(blank=True, to='dashboard.campus'),
        ),
        migrations.AddField(
            model_name='notices',
            name='departments',
            field=models.ManyToManyField(blank=True, to='dashboard.department'),
        ),
        migrations.AddField(
            model_name='notices',
            name='programs',
            field=models.ManyToManyField(blank=True, to='dashboard.program'),
        ),
        migrations.AddField(
            model_name='notices',
            name='recipient_type',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('both', 'Both')], default='student', max_length=10),
        ),
        migrations.AlterField(
            model_name='notices',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
