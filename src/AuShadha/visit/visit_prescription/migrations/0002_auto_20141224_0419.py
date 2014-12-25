# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit_prescription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitprescription',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name=b'Treatment End Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitprescription',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name=b'Treatment Start Date', blank=True),
            preserve_default=True,
        ),
    ]
