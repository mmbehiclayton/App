# Generated by Django 3.1.1 on 2023-05-15 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_staff_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.classes', verbose_name='Assign Class'),
        ),
    ]
