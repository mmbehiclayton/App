# Generated by Django 4.2.1 on 2023-05-17 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_exam_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exammeanresult',
            name='teacher',
        ),
    ]
