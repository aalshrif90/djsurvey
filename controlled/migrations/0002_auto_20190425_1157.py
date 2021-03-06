# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-25 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlled', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testsuite',
            name='code',
        ),
        migrations.AddField(
            model_name='testsuite',
            name='other_label',
            field=models.CharField(choices=[('OR', 'Non-reduced'), ('RD', 'Redcued')], default='OR', max_length=255),
        ),
        migrations.AlterField(
            model_name='testsuite',
            name='automated',
            field=models.BooleanField(default=True, help_text='Automated or Manual?'),
        ),
    ]
