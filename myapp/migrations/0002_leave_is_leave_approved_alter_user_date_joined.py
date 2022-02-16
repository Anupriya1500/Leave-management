# Generated by Django 4.0.2 on 2022-02-16 16:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='is_leave_approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 16, 16, 38, 10, 210250, tzinfo=utc)),
        ),
    ]
