# Generated by Django 3.1.1 on 2021-01-14 09:36

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
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
