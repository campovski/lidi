# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-24 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0002_user_conf_link'),
        ('problem', '0005_auto_20180124_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='first_solved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_solved_by', to='signup.User'),
        ),
        migrations.AddField(
            model_name='problem',
            name='first_solved_on',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='last_successful_try',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='solved_by_how_many',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='submitted_on',
            field=models.DateField(default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='problem',
            name='submitted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_by', to='signup.User'),
        ),
    ]
