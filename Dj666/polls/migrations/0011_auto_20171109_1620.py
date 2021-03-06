# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 08:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_sub_teach'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mdesc', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sub1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teach1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('members', models.ManyToManyField(through='polls.Membership', to='polls.Sub1')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='sub1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Sub1'),
        ),
        migrations.AddField(
            model_name='membership',
            name='teach1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Teach1'),
        ),
    ]
