# Generated by Django 3.1.1 on 2020-11-25 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 25, 20, 16, 16, 127124), null=True),
        ),
    ]
