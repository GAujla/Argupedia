# Generated by Django 3.2.5 on 2021-08-29 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Argupedia', '0002_auto_20210828_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='argprofile',
            name='pict',
        ),
        migrations.AddField(
            model_name='argprofile',
            name='profile_picture',
            field=models.ImageField(default='default.png', upload_to='arguserpic'),
        ),
    ]
