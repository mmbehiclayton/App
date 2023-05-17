# Generated by Django 4.2.1 on 2023-05-16 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_rename_name_sessionterm_term_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sessionterm',
            name='name',
            field=models.CharField(choices=[('Term 1', 'Term 1'), ('Term 2', 'Term 2'), ('Term 3', 'Term 3')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='classes',
            name='name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sessionterm',
            name='term',
            field=models.CharField(choices=[('First Term', 'First Term'), ('Second Term', 'Second Term'), ('Third Term', 'Third Term')], max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='class_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.classes', verbose_name='class'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
