# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-10 16:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controlled', '0015_answeredtestcases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answeredtestcases',
            name='duration',
        ),
    ]