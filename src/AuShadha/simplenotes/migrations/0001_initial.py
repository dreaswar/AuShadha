# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleNotes_FirstVisit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complaints', models.TextField(max_length=300)),
                ('history_of_present_illness', models.TextField(max_length=1000, null=True, blank=True)),
                ('past_history', models.TextField(max_length=500, null=True, blank=True)),
                ('treatment_history', models.TextField(max_length=500, null=True, blank=True)),
                ('birth_history', models.TextField(max_length=500, null=True, blank=True)),
                ('family_history', models.TextField(max_length=500, null=True, blank=True)),
                ('personal_history', models.TextField(max_length=500, null=True, blank=True)),
                ('regional_examination', models.TextField(max_length=500)),
                ('systemic_examination', models.TextField(default=b'NAD', max_length=500)),
                ('vitals', models.TextField(max_length=250, null=True, blank=True)),
                ('investigation_notes', models.TextField(max_length=500, null=True, blank=True)),
                ('summary', models.TextField(max_length=500)),
                ('diagnosis', models.TextField(max_length=500)),
                ('plan', models.TextField(max_length=500)),
                ('visit_detail', models.ForeignKey(to='visit.VisitDetail')),
            ],
            options={
                'ordering': ('complaints', 'history_of_present_illness', 'past_history', 'treatment_history', 'birth_history', 'family_history', 'personal_history', 'regional_examination', 'systemic_examination', 'vitals', 'investigation_notes', 'summary', 'diagnosis', 'plan'),
                'verbose_name': 'Simple Visit Notes- First Visit',
                'verbose_name_plural': 'Simple Visit Notes- First Visit',
            },
            bases=(models.Model,),
        ),
    ]
