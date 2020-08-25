# Generated by Django 3.1 on 2020-08-20 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_auto_20200819_1034'),
        ('blog', '0007_remove_blogpost_related_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='related_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.eventpost'),
        ),
    ]