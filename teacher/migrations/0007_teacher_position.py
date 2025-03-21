# Generated by Django 5.1.1 on 2025-02-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_alter_teacher_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='position',
            field=models.CharField(choices=[('instructor', 'Instructor'), ('senior_instr', 'Senior Instructor'), ('chief_inst', 'Chief Instructor'), ('deputy_hod', 'Deputy HOD'), ('hod', 'HOD'), ('principal', 'Principal')], default=1, max_length=100),
            preserve_default=False,
        ),
    ]
