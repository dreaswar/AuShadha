#
# PROJECT: AuShadha ICD10 Procedure Code Models
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
#

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from django.contrib.auth.models import User
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel


from AuShadha.apps.clinic.models import Clinic


# ICD10 PROCEDURE CODE MODELS ############################################

class PcsTable(models.Model):

    """The ICD10 pcsTable model."""

    __model_label__ = "pcs_table"

    sec_id = models.PositiveIntegerField(
        "Section ID", max_length=200, unique=True)
    section = models.CharField(
        'Section', max_length=200, null=True, blank=True)
    body_system = models.CharField(
        'Body System', max_length=200, null=True, blank=True)
    operation = models.CharField(
        'Operation', max_length=200, null=True, blank=True)

# Define the Unicode method ::
    def __unicode__(self):
        return "%s: %s - %s" % (self.section, self.body_system, self.operation)


class PcsRow(models.Model):

    """The ICD 10 Procedure Code Rows."""

    __model_label__ = "pcs_row"
    pcsRow_id = models.PositiveIntegerField(
        'pcsRow_id', max_length=200, unique=True)
    pcsTable_fk = models.ForeignKey('PcsTable')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s" % (self.pcsRow_id)


class BodyPart(models.Model):

    """The ICD 10 PCS bodypart models."""

    __model_label__ = "body_part"

    body_part = models.CharField(
        'Body Part', max_length=200, null=True, blank=True)
    pcsRow_fk = models.ForeignKey('PcsRow')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s" % (self.body_part)


class Approach(models.Model):

    """The ICD 10 PCS approach models."""

    __model_label__ = "approach"

    approach = models.CharField(
        'Approach', max_length=200, null=True, blank=True)
    pcsRow_fk = models.ForeignKey('PcsRow')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s" % (self.approach)


class Device(models.Model):

    """The ICD 10 PCS bodypart models."""

    __model_label__ = "device"

    device = models.CharField(
        'Device', max_length=200, null=True, blank=True)
    pcsRow_fk = models.ForeignKey('PcsRow')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s" % (self.device)


class Qualifier(models.Model):

    """The ICD 10 PCS qualifier models."""

    __model_label__ = "qualifier"

    qualifier = models.CharField(
        'Qualifier', max_length=200, null=True, blank=True)
    pcsRow_fk = models.ForeignKey('PcsRow')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s" % (self.qualifier)
