# Generated by Django 3.1.1 on 2023-05-15 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.session')),
            ],
        ),
    ]
