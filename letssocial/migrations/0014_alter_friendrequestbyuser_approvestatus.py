# Generated by Django 3.2.10 on 2022-08-03 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0013_friendrequestbyuser_userwhorequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequestbyuser',
            name='approvestatus',
            field=models.CharField(choices=[('norespond', 'No Respond'), ('reject', 'Rejected'), ('accept', 'Accepted'), ('block', 'Blocked'), ('cancel', 'Cancel Request')], default='norespond', max_length=300),
        ),
    ]
