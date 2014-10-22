# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_hospital_id', models.CharField(unique=True, max_length=15, verbose_name=b'Hospital ID')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(help_text=b'Please enter Initials / Middle Name', max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(help_text=b'Enter Initials / Last Name', max_length=30, null=True, blank=True)),
                ('full_name', models.CharField(max_length=100, editable=False)),
                ('age', models.CharField(max_length=10, null=True, blank=True)),
                ('sex', models.CharField(default=b'Male', max_length=6, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'Others', b'Others')])),
                ('parent_clinic', models.ForeignKey(to='clinic.Clinic')),
            ],
            options={
                'ordering': ('first_name', 'middle_name', 'last_name', 'age', 'sex', 'patient_hospital_id'),
                'verbose_name': 'Patient - Basic Data',
                'verbose_name_plural': 'Patient - Basic Data',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='patientdetail',
            unique_together=set([('patient_hospital_id', 'parent_clinic')]),
        ),
    ]
