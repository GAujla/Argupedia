# Generated by Django 2.2.7 on 2021-08-04 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ArgUsers', '0003_argprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='argprofile',
            old_name='ArgPic',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='argprofile',
            old_name='Arguser',
            new_name='user',
        ),
    ]
