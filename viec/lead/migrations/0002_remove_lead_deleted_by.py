# Generated by Django 3.0.2 on 2020-01-18 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='deleted_by',
        ),
    ]
