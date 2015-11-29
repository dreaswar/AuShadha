# -*- coding: utf-8 -*-
###############################################################
# PROJECT: AuShadha ICD10 Procedure Code Models
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################
"""
 =============================== Axis Labels

 Axes 1..3: Table Axis Labels (AKA "Code Page")
 Axes 4..7: Row Axis Labels

 Common Fields:
    codepage
    code
    label_fk
    title_fk

 Axis Specific Fields:
    Axis 3, Operation
        defn_fk
    Row Axis Labels
        row_num
        pos

 Ordering:
    Table Axis Labels: codepage, code
    Row Axis Labels: codepage, row_num, pos, code

 Generic Axis Names:
    sections,
    body_systems,
    operations,
    body_parts,
    approaches,
    devices,
    qualifiers,

"""

#======================================================================
# IMPORTS

from django.db import models
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel

#======================================================================
# CONSTANTS

MANAGED_FLAG = True

SINGLE_CHAR = 1
SHORT_CHARS = 100
LONG_CHARS = 1000

CODEPAGE_CHARS = 3

CODEPAGE_ROW_CHARS = 7  # Ex: "0B2-1", "...-64" (pseudo composite key)

REMAP_FIELDS = True


#======================================================================
# MODELS: Configuration & Unique Text

class AppCfg(models.Model):
    id = models.IntegerField(primary_key=True)
    cfg_key = models.CharField(max_length=SHORT_CHARS)
    cfg_value = models.CharField(max_length=SHORT_CHARS)

    class Meta:
        managed = MANAGED_FLAG


class AppTxt(models.Model):
    id = models.IntegerField(primary_key=True)
    txt = models.CharField(max_length=LONG_CHARS)

    class Meta:
        managed = MANAGED_FLAG


#======================================================================
# MANAGERS/QUERYSETS: For chainable queries

# ToDo: Definition text for axis 3 (hover-over text?)

# Friendly field names:
remap = lambda d: {'code': d['code'],
                   'label': d['label_fk__txt'],
                   'title': d['title_fk__txt'],
                   #                    'defn': d['defn_fk__txt'],
                   }


class TableAxisLabelMixin(object):

    def as_labels(self, distinct=False):
        r = self.order_by('code') .values(
            'code', 'label_fk__txt', 'title_fk__txt')  # , 'defn_fk.txt')
        if distinct:
            r = r.distinct()
        if REMAP_FIELDS:
            r = [remap(l) for l in r]
        return r

    def by_codepage(self, codepage, remap_fields=False):
        """Filter, order, distinct, values: code, label, title (remapped)"""
        codepage = str(codepage).upper()  # YAML: "0" becomes 0
        objs = self
        if codepage != '':
            objs = objs.filter(codepage__startswith=codepage)
        return objs.as_labels(distinct=True)

    def by_codepage_row(self, codepage, row_num, remap_fields=False):
        """Filter, order, distinct, values: code, label, title (remapped)"""

        if len(codepage) != 3:
            return []

        codepage = str(codepage).upper()  # YAML: "0" becomes 0
        objs = self.filter(codepage=codepage, row_num=row_num)
        return objs.as_labels()


class TableAxisLabelQuerySet(QuerySet, TableAxisLabelMixin):
    pass


class TableAxisLabelManager(models.Manager, TableAxisLabelMixin):

    def get_query_set(self):
        return TableAxisLabelQuerySet(self.model, using=self._db)


#======================================================================
# ABSTRACT MODELS: Table and row axis labels very similar so...

class TableAxisLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    codepage = models.CharField(max_length=CODEPAGE_CHARS)
    code = models.CharField(max_length=SINGLE_CHAR)
    label_fk = models.ForeignKey('AppTxt', related_name='+')
    title_fk = models.ForeignKey('AppTxt', related_name='+')

    objects = TableAxisLabelManager()

    def __unicode__(self):
        return "%s %s" % (self.code, getattr(self, 'label_fk.txt', ''))

    class Meta:
        ordering = ['codepage', 'code']
        abstract = True


class RowAxisLabel(TableAxisLabel, TableAxisLabelMixin):
    row_id = models.ForeignKey('CodePageRow')
    row_num = models.PositiveIntegerField()
    pos = models.PositiveIntegerField()

    class Meta:
        ordering = ['codepage', 'row_num', 'pos', 'code']
        abstract = True


#======================================================================
# MODELS: Table axis labels, first three axes

class Section(TableAxisLabel, AuShadhaBaseModel):
    pass


class BodySystem(TableAxisLabel, AuShadhaBaseModel):
    pass


class Operation(TableAxisLabel, AuShadhaBaseModel):
    defn_fk = models.ForeignKey('AppTxt', related_name='+')


#======================================================================
# MODELS: Code Page rows and row axis labels, axes 4..7


class CodePageRow(models.Model):
    id = models.CharField(max_length=CODEPAGE_ROW_CHARS, primary_key=True)
    codepage = models.CharField(max_length=CODEPAGE_CHARS)
    row_num = models.IntegerField()

    class Meta:
        managed = MANAGED_FLAG


class BodyPart(RowAxisLabel):
    pass


class Approach(RowAxisLabel):
    pass


class Device(RowAxisLabel):
    pass


class Qualifier(RowAxisLabel):
    pass
