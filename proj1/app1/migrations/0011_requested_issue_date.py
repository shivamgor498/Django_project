# Generated by Django 2.0.4 on 2018-07-22 08:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20180722_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='requested',
            name='issue_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 22, 8, 6, 20, 41932)),
        ),
    ]
