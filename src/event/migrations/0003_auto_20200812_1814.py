# Generated by Django 3.1 on 2020-08-12 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200812_1714'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='EventCategory',
        ),
    ]
