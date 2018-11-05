# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 16:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20171123_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='schema',
            field=models.ForeignKey(blank=True, help_text='Choose a Schema', null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Schema'),
        ),
    ]
