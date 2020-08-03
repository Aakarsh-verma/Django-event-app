# Generated by Django 3.0.8 on 2020-08-01 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20200801_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='category',
            field=models.CharField(choices=[('COMP/IT', 'Computer'), ('EXTC/ETRX', 'Electrical'), ('MECH/AUTO', 'Mechanical'), ('ALL', 'All'), ('NON-TECH', 'Non-Technical'), ('', '')], default='All', max_length=10),
        ),
        migrations.AlterField(
            model_name='eventpost',
            name='category2',
            field=models.CharField(choices=[('COMP/IT', 'Computer'), ('EXTC/ETRX', 'Electrical'), ('MECH/AUTO', 'Mechanical'), ('ALL', 'All'), ('NON-TECH', 'Non-Technical'), ('', '')], default='', max_length=10),
        ),
    ]