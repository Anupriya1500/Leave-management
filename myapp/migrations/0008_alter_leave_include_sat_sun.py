# Generated by Django 4.0.2 on 2022-03-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_leave_include_sat_sun_alter_leave_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='include_sat_sun',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]