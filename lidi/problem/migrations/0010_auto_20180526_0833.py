# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0009_auto_20180524_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='submitted_on',
            field=models.CharField(default=b'2018-5-26', max_length=10),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.CharField(default=b'2018-5-26', max_length=10),
        ),
    ]
