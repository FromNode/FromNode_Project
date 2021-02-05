# Generated by Django 3.1.3 on 2021-02-04 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NodeApp', '0002_auto_20210108_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('author_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('node_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NodeApp.nodes')),
            ],
        ),
    ]
