# Generated by Django 3.1.1 on 2023-05-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_classes_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
