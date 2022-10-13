# Generated by Django 3.2.10 on 2022-09-19 18:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0027_auto_20220919_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replycomments',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 19, 18, 12, 21, 600010, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='savechats',
            name='messagetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 19, 18, 12, 21, 600010, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usercomments',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 19, 18, 12, 21, 600010, tzinfo=utc)),
        ),
    ]
