# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuShadhaUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('aushadha_user_role', models.CharField(default=b'aushadha_user', help_text=b' Users Role in AuShadha Software.\n                                                           This is different from the role in the Clinic', max_length=30, verbose_name=b'AuShadha User Role', choices=[(b'audhadha_admin', b'AuShadha Admin'), (b'aushadha_user', b'AuShadha User'), (b'aushadha_staff', b'AuShadha Staff '), (b'aushadha_developer', b'AuShadha Developer')])),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
    ]
