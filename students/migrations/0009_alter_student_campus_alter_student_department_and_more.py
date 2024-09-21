# Generated by Django 5.1.1 on 2024-09-21 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('students', '0008_student_kiosk_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='campus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.campus'),
        ),
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.program'),
        ),
        migrations.AlterField(
            model_name='student',
            name='shift',
            field=models.CharField(blank=True, choices=[('MORNING', 'Morning'), ('AFTERNOON', 'Afternoon'), ('EVENING', 'Evening')], max_length=50, null=True),
        ),
    ]
