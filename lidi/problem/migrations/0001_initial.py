# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 13:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=6000)),
                ('difficulty', models.IntegerField()),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.User')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('tries', models.IntegerField()),
                ('is_solved', models.BooleanField(default=False)),
                ('sub_file', models.CharField(max_length=100)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.User')),
            ],
        ),
    ]
