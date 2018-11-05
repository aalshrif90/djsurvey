# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-27 13:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20171206_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of Group', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GroupQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technique', models.CharField(blank=True, choices=[('DOMINO', 'Domino'), ('SELECTOR', 'Selector'), ('SOURCER', 'Sourcer'), ('READER', 'Reader'), ('COLNAMER', 'ColumnNamer'), ('AVMLM', 'AVM-LM'), ('AVMR', 'AVM-R'), ('AVMD', 'AVM-D')], max_length=255, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Group')),
                ('schema', models.ForeignKey(blank=True, help_text='Choose a Schema', null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Schema')),
            ],
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(help_text='The code given to a user', max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Group')),
            ],
        ),
    ]
