# Generated by Django 4.2.11 on 2024-04-06 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_patientreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='doctor_language',
            field=models.CharField(default='english', max_length=20),
            preserve_default=False,
        ),
    ]
