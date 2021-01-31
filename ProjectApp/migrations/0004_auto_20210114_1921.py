# Generated by Django 3.1.1 on 2021-01-14 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProjectApp', '0003_proj_with_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proj_with_user',
            name='proj_id',
            field=models.ForeignKey(db_column='proj_id', on_delete=django.db.models.deletion.CASCADE, to='ProjectApp.projects'),
        ),
        migrations.AlterField(
            model_name='proj_with_user',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]