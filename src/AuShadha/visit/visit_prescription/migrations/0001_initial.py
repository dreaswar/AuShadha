# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminHours',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
            ],
            options={},
            bases=(
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name='DispensingForms',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
            ],
            options={},
            bases=(
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
            ],
            options={},
            bases=(
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
            ],
            options={},
            bases=(
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
            ],
            options={},
            bases=(
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name='VisitPrescription',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
                ('medicament',
                 models.TextField(
                     default=b'',
                     max_length=100)),
                ('indication',
                 models.TextField(
                     default=b'',
                     max_length=100,
                     null=True,
                     blank=True)),
                ('allow_substitution',
                 models.BooleanField(
                     default=False)),
                ('print_prescription',
                 models.BooleanField(
                     default=False)),
                ('dispensing_form',
                 models.CharField(
                     default=b'Tablet',
                     max_length=30,
                     choices=[
                         (b'tablet',
                          b'Tablet'),
                         (b'dispersible_tablet',
                          b'Dispersible Tablet'),
                         (b'chewable_tablet',
                          b'Chewable Tablet'),
                         (b'capsule',
                          b'Capsule'),
                         (b'suspension',
                          b'Suspension'),
                         (b'dry_syrup',
                          b'Dry Syrup'),
                         (b'injection',
                          b'Injection'),
                         (b'spray',
                          b'Spray'),
                         (b'inhaler',
                          b'Inhaler'),
                         (b'gargle',
                          b'Gargle'),
                         (b'drops',
                          b'Drops'),
                         (b'ointment',
                          b'Ointment'),
                         (b'gel',
                          b'Gel'),
                         (b'liniment',
                          b'Liniment'),
                         (b'suppository',
                          b'Suppository')])),
                ('route',
                 models.CharField(
                     default=b'Oral',
                     max_length=30,
                     choices=[
                         (b'oral',
                          b'Oral'),
                         (b'sub_lingual',
                          b'Sub-Lingual'),
                         (b'intra_nasal',
                          b'Intra Nasal'),
                         (b'into_the_eye',
                          b'Into the Eye'),
                         (b'into_the_ear',
                          b'Into the Ear'),
                         (b'per_rectal',
                          b'Per Rectal'),
                         (b'per_vaginal',
                          b'Per Vaginal'),
                         (b'topical_application',
                          b'Topical Application'),
                         (b'intra_oral_application',
                          b'Intra Oral Application'),
                         (b'gargle',
                          b'Gargle'),
                         (b'sub_cutaneous',
                          b'Sub-Cutaneous'),
                         (b'intra_muscular',
                          b'Intra Muscular'),
                         (b'intra_muscular',
                          b'Intra Articular'),
                         (b'intra_osseous',
                          b'Intra Osseous'),
                         (b'intra_venous',
                          b'Intra Venous'),
                         (b'intra_arterial',
                          b'Intra Arterial')])),
                ('start_date',
                 models.DateTimeField(
                     auto_now=True,
                     verbose_name=b'Treatment Start Date',
                     null=True)),
                ('end_date',
                 models.DateTimeField(
                     auto_now=True,
                     verbose_name=b'Treatment End Date',
                     null=True)),
                ('treatment_duration',
                 models.CharField(
                     max_length=30,
                     null=True,
                     blank=True)),
                ('dose',
                 models.CharField(
                     max_length=30)),
                ('dose_unit',
                 models.CharField(
                     max_length=30,
                     verbose_name=b'Unit',
                     choices=[
                         (b'g',
                          b'gram'),
                         (b'mg',
                          b'MG'),
                         (b'micro_gram',
                          b'Micro Gram'),
                         (b'ml',
                          b'ml'),
                         (b'mmol',
                          b'mmol'),
                         (b'drops',
                          b'Drops'),
                         (b'iu',
                          b'IU'),
                         (b'u',
                          b'U')])),
                ('units',
                 models.PositiveIntegerField(
                     help_text=b'Quantity of medications to be given;                                   like number of tablets/ capsules',
                     max_length=3)),
                ('frequency',
                 models.CharField(
                     default=b'',
                     max_length=30,
                     choices=[
                         (b'once_a_month',
                          b'Once a Month'),
                         (b'once_a_week',
                          b'Once a Week'),
                         (b'once_every_alternate_day',
                          b'Once every alternate Day'),
                         (b'once_a_day',
                          b'Once a Day'),
                         (b'every_twelth_hourly',
                          b'Every 12 Hours'),
                         (b'every_eight_hourly',
                          b'Every 8 Hours'),
                         (b'every_sixth_hourly',
                          b'Every 6 hours'),
                         (b'every_fourth_hourly',
                          b'Every 4 Hours'),
                         (b'every_two_hourly',
                          b'Every 2 Hours'),
                         (b'every_hour',
                          b'Every One Hour'),
                         (b'at_bed_time',
                          b'At Bed Time'),
                         (b'early_morning',
                          b'Early Morning'),
                         (b'after_noon',
                          b'After Noon'),
                         (b'sos',
                          b'S.O.S'),
                         (b'as_required',
                          b'As Needed'),
                         (b'stat',
                          b'Stat')])),
                ('admin_hours',
                 models.TextField(
                     default=b'',
                     max_length=250)),
                ('review',
                 models.DateTimeField(
                     null=True,
                     blank=True)),
                ('refills',
                 models.PositiveIntegerField(
                     default=0,
                     max_length=2)),
                ('comment',
                 models.TextField(
                     default=b'',
                     max_length=300,
                     null=True,
                     blank=True)),
                ('visit_detail',
                 models.ForeignKey(
                     blank=True,
                     to='visit.VisitDetail',
                     null=True)),
            ],
            options={
                'verbose_name': 'Visit Prescription',
                'verbose_name_plural': 'Visit Prescription',
            },
            bases=(
                models.Model,
            ),
        ),
    ]
