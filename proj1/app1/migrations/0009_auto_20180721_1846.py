# Generated by Django 2.0.4 on 2018-07-21 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20180721_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requested',
            old_name='author',
            new_name='requestedBy',
        ),
    ]
