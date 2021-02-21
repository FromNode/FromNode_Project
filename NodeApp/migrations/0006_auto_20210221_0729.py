# Generated by Django 3.1.1 on 2021-02-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NodeApp', '0005_auto_20210218_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodes',
            name='nodeName',
        ),
        migrations.AddField(
            model_name='nodes',
            name='added_letters',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='added_sentences',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='is_workflow',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='similarity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
