# Generated by Django 3.1 on 2020-08-12 11:44

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="eventpost",
            name="category",
            field=models.CharField(default="null", max_length=100),
        ),
        migrations.AlterField(
            model_name="eventpost",
            name="image",
            field=models.ImageField(
                default="logo.png", upload_to=event.models.upload_location
            ),
        ),
    ]
