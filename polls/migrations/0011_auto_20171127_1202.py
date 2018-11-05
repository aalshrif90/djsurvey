# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_randomisedanswersorder_answered'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='randomisedanswersorder',
            options={'ordering': ['timestamp']},
        ),
        migrations.AddField(
            model_name='randomisedanswersorder',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
