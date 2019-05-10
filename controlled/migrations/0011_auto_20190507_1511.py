# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-07 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlled', '0010_auto_20190430_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dropdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dropdown_text', models.CharField(help_text='Added your Dropdown text here.', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='dropdown',
            field=models.BooleanField(default=False, help_text='Drop-down question?'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test_suite',
            field=models.ForeignKey(blank=True, help_text='Choose a Test Suite', null=True, on_delete=django.db.models.deletion.CASCADE, to='controlled.TestSuite'),
        ),
        migrations.AddField(
            model_name='dropdown',
            name='question',
            field=models.ForeignKey(help_text='Choose a question.', on_delete=django.db.models.deletion.CASCADE, related_name='question_dropdown', to='controlled.Question'),
        ),
    ]