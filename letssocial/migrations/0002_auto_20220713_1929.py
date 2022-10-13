# Generated by Django 3.2.10 on 2022-07-13 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useruploadedimage',
            name='imageuser',
        ),
        migrations.AddField(
            model_name='useruploadedimage',
            name='imageusername',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='useruploadedimage',
            name='uploadedimage',
            field=models.ImageField(upload_to='letsocial/<django.db.models.fields.CharField>'),
        ),
    ]
