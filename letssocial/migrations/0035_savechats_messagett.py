# Generated by Django 3.2.10 on 2022-09-21 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0034_savechats_messagedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='savechats',
            name='messagett',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
