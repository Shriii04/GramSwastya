# Generated by Django 4.2.11 on 2024-04-06 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0009_patientreport_age_patientreport_gender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='user',
        ),
    ]
