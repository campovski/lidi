# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-28 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0010_auto_20180526_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='submitted_on',
            field=models.CharField(default=b'2018-5-28', max_length=10),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.CharField(default=b'2018-5-28', max_length=10),
        ),
    ]