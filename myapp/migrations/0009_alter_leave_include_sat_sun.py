# Generated by Django 4.0.2 on 2022-03-01 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_leave_include_sat_sun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='include_sat_sun',
            field=models.BooleanField(default=False),
        ),
    ]
