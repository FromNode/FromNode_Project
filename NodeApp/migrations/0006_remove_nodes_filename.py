# Generated by Django 3.1.1 on 2021-01-23 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NodeApp', '0005_auto_20210123_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodes',
            name='filename',
        ),
    ]
