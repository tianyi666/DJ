# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vft', '0002_auto_20171201_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('desc', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('sex', models.BooleanField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vft.School')),
            ],
        ),
        migrations.AlterModelOptions(
            name='panda',
            options={'verbose_name': '熊猫'},
        ),
        migrations.AlterField(
            model_name='panda',
            name='sex',
            field=models.IntegerField(choices=[(1, '男'), (0, '女')]),
        ),
    ]
