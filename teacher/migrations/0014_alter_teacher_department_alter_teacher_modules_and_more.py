# Generated by Django 5.2 on 2025-05-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_campus_code_alter_department_code_and_more'),
        ('teacher', '0013_remove_teacher_campus_remove_teacher_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='department',
            field=models.ManyToManyField(blank=True, to='dashboard.department'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='modules',
            field=models.ManyToManyField(blank=True, to='dashboard.modules'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='program',
            field=models.ManyToManyField(blank=True, to='dashboard.program'),
        ),
    ]
