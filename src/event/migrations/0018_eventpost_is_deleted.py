# Generated by Django 3.1 on 2020-08-29 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0017_auto_20200820_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpost',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
