# Generated by Django 3.2.10 on 2022-09-19 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0024_auto_20220919_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replycomments',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 19, 23, 38, 28, 605502)),
        ),
        migrations.AlterField(
            model_name='savechats',
            name='messagetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 19, 23, 38, 28, 606502)),
        ),
        migrations.AlterField(
            model_name='usercomments',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 19, 23, 38, 28, 604502)),
        ),
    ]
