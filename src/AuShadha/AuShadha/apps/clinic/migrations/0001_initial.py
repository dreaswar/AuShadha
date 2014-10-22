# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aushadha_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('building_no', models.CharField(default=b'Tamil Nadu', max_length=200)),
                ('street_name', models.TextField()),
                ('city_or_town', models.CharField(default=b'Coimbatore', max_length=200)),
                ('district', models.CharField(default=b'Coimbatore', max_length=200)),
                ('state', models.CharField(default=b'Tamil Nadu', max_length=200)),
                ('country', models.CharField(default=b'India', max_length=200)),
                ('postal_code', models.CharField(max_length=200, verbose_name=b'Postal Code')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_of_clinic', models.CharField(max_length=200)),
                ('nature_of_clinic', models.CharField(max_length=200, choices=[(b'primary_health_centre', b'Primary Health Centre'), (b'community_health_centre', b'Community Health Centre'), (b'poly_clinic', b'Poly Clinic'), (b'speciality_clinic', b'Speciality Clinic'), (b'district_hospital', b'District Hospital'), (b'tertiary_referral_centre', b'Tertiary Referral Centre')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_of_department', models.CharField(unique=True, max_length=100)),
                ('clinic', models.ForeignKey(to='clinic.Clinic')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_address', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(to='clinic.Clinic')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fax_number', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(to='clinic.Clinic')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_code', models.PositiveIntegerField(default=91, max_length=6)),
                ('area_code', models.PositiveIntegerField(default=422, max_length=10)),
                ('phone_number', models.PositiveIntegerField(max_length=200)),
                ('clinic', models.ForeignKey(to='clinic.Clinic')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clinic_staff_role', models.CharField(help_text=b' This is the Role of the Staff in the Clinic', max_length=100, verbose_name=b'Staff Role', choices=[(b'non_clinical_staff', b'Non Clinical Staff'), (b'secretary', b'Secretary'), (b'clinic_admin', b'Clinic Administrator'), (b'clinical_staff', b'Clinical Staff'), (b'nurse', b'Nurse'), (b'physio', b'Physiotherapist'), (b'doctor', b'Doctor')])),
                ('is_staff_hod', models.BooleanField(default=None, verbose_name=b'Is Staff Head of the Department')),
                ('department', models.ForeignKey(to='clinic.Department')),
                ('staff_detail', models.ForeignKey(to='aushadha_users.AuShadhaUser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website_address', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(to='clinic.Clinic')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='clinic',
            field=models.ForeignKey(to='clinic.Clinic'),
            preserve_default=True,
        ),
    ]
