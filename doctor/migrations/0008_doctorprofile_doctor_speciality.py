# Generated by Django 4.2.11 on 2024-04-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_doctorprofile_doctor_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='doctor_speciality',
            field=models.CharField(default='physician', max_length=30),
            preserve_default=False,
        ),
    ]
