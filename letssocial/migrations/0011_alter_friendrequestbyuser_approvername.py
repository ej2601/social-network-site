# Generated by Django 3.2.10 on 2022-08-03 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('letssocial', '0010_alter_friendrequestbyuser_approvestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequestbyuser',
            name='approvername',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letssocial.userprofileimage'),
        ),
    ]
