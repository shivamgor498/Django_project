# Generated by Django 2.0.4 on 2018-07-28 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_auto_20180728_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requested',
            name='return_date',
            field=models.DateField(default=datetime.date(2018, 8, 4)),
        ),
    ]
