# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 06:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20171108_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='maker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mk', to='polls.Maker'),
        ),
    ]
