# Generated by Django 3.2.10 on 2022-09-19 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0028_auto_20220919_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replycomments',
            name='pub_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='savechats',
            name='messagetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='usercomments',
            name='pub_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
