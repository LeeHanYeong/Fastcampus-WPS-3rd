# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('invite_reason', models.CharField(max_length=64)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='album',
            name='artist',
        ),
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Musician',
        ),
        migrations.AddField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Person'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='music.Membership', to='music.Person'),
        ),
    ]
