# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-28 06:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='signup.Category'),
        ),
    ]
