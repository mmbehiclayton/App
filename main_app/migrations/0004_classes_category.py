# Generated by Django 4.2.1 on 2023-05-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_classes_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='category',
            field=models.CharField(choices=[('lower classes (1-3)', 'lower classes (1-3)'), ('middle classes (4-6)', 'middle classes (4-6)'), ('Junior Secondary', 'Junior Secondary')], max_length=20, null=True),
        ),
    ]