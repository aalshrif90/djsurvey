# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-30 10:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlled', '0004_auto_20190425_1603'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RandomisedAnswersOrder',
            new_name='RandomiseQuestions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_category',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='question',
            field=models.ForeignKey(default=0, help_text='Question', on_delete=django.db.models.deletion.CASCADE, to='controlled.Question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questiontext',
            name='question',
            field=models.ForeignKey(default=None, help_text='Question', on_delete=django.db.models.deletion.CASCADE, to='controlled.Question'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='score',
            field=models.IntegerField(default=0, help_text='Score'),
        ),
    ]
