# Generated by Django 5.1.1 on 2025-02-27 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0009_teacher_category_alter_teacher_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='position',
            field=models.CharField(choices=[('instructor', 'Instructor'), ('senior_instr', 'Senior Instructor'), ('chief_inst', 'Chief Instructor'), ('deputy_hod', 'Deputy HOD'), ('hod', 'HOD'), ('principal', 'Principal'), ('assistant', 'Assistant'), ('officer', 'Officer'), ('senior_officer', 'Senior Officer'), ('chief_officer', 'Chief Officer'), ('deputy_hod', 'Deputy HOD'), ('hod', 'HOD'), ('executive_director', 'Executive Director')], max_length=100),
        ),
    ]
