# Generated by Django 3.1.1 on 2021-04-11 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NodeApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodes',
            name='ownerFCode',
        ),
    ]
