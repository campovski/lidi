# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-24 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20170605_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.CharField(default=b'2018/1/24', max_length=10),
        ),
    ]
