# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-30 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlled', '0005_auto_20190430_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncategory',
            name='question',
            field=models.ForeignKey(blank=True, help_text='Question', null=True, on_delete=django.db.models.deletion.CASCADE, to='controlled.Question'),
        ),
        migrations.AlterField(
            model_name='questiontext',
            name='question',
            field=models.ForeignKey(blank=True, help_text='Question', null=True, on_delete=django.db.models.deletion.CASCADE, to='controlled.Question'),
        ),
    ]
