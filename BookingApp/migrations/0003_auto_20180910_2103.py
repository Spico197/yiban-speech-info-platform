# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-10 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0002_auto_20180910_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='stu_number',
            field=models.TextField(),
        ),
    ]