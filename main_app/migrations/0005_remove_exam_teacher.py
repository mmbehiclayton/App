# Generated by Django 4.2.1 on 2023-05-19 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_classes_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='teacher',
        ),
    ]