# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-30 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlled', '0009_auto_20190430_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questioncategory',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questiontext',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='question_category',
            field=models.ForeignKey(blank=True, help_text='Question Category', null=True, on_delete=django.db.models.deletion.CASCADE, to='controlled.QuestionCategory'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.ForeignKey(blank=True, help_text='Question Text', null=True, on_delete=django.db.models.deletion.CASCADE, to='controlled.QuestionText'),
        ),
    ]
