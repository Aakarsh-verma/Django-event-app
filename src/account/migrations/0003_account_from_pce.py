# Generated by Django 3.1 on 2020-08-13 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_is_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='from_pce',
            field=models.BooleanField(default=True),
        ),
    ]
