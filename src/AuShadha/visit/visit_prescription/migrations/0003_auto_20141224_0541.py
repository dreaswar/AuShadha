# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit_prescription', '0002_auto_20141224_0419'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitprescription',
            options={'ordering': ['print_prescription', 'allow_substitution', 'dispensing_form', 'medicament', 'indication', 'dose', 'dose_unit', 'frequency', 'admin_hours', 'route', 'start_date', 'end_date', 'treatment_duration', 'units', 'refills', 'comment'], 'verbose_name': 'Visit Prescription', 'verbose_name_plural': 'Visit Prescription'},
        ),
        migrations.AlterField(
            model_name='visitprescription',
            name='admin_hours',
            field=models.TextField(default=b'', max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
