# Generated by Django 4.2.1 on 2023-05-11 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth_tasks', '0002_alter_task_date_completed_alter_task_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 12, 36, 47, 603041)),
        ),
    ]