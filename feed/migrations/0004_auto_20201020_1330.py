# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-20 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('feed', '0003_image_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image_comment',
            name='user',
        ),
        migrations.AddField(
            model_name='image_comment',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
            preserve_default=False,
        ),
    ]
