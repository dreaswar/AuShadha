# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit_prescription', '0003_auto_20141224_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitprescription',
            name='frequency',
            field=models.CharField(max_length=30, choices=[(b'once_a_month', b'Once a Month'), (b'once_a_week', b'Once a Week'), (b'once_every_alternate_day', b'Once every alternate Day'), (b'once_a_day', b'Once a Day'), (b'every_twelth_hourly', b'Every 12 Hours'), (b'every_eight_hourly', b'Every 8 Hours'), (b'every_sixth_hourly', b'Every 6 hours'), (b'every_fourth_hourly', b'Every 4 Hours'), (b'every_two_hourly', b'Every 2 Hours'), (b'every_hour', b'Every One Hour'), (b'at_bed_time', b'At Bed Time'), (b'early_morning', b'Early Morning'), (b'after_noon', b'After Noon'), (b'sos', b'S.O.S'), (b'as_required', b'As Needed'), (b'stat', b'Stat')]),
        ),
    ]
