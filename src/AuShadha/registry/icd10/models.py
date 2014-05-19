#
# PROJECT: AuShadha ICD10 Models
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


class Chapter(models.Model):

    '''
    The ICD 10 Chapters and the sub-fields.
    Most fields are incorporated.
    Some fields may have been ignored.
    This is as good as the parser that was built to get the data out.

    '''

    __model_label__ = "icd10_chapter"

    chapter_name = models.TextField(
        'Chapter Name', max_length=1000, null=True, blank=True)
    chapter_desc = models.TextField(
        'Chapter Description', max_length=1000, null=True, blank=True)
    includes = models.TextField(
        'Includes', max_length=1000, null=True, blank=True)
    useAdditionalCode = models.TextField(
        'Use Additional Codes', max_length=1000, null=True, blank=True)
    excludes1 = models.TextField(
        'Excludes 1', max_length=1000, null=True, blank=True)
    excludes2 = models.TextField(
        'Excludes 2', max_length=1000, null=True, blank=True)
    sectionIndex = models.TextField(
        'Section Index', max_length=1000, null=True, blank=True)

# Define the Unicode method ::
    def __unicode__(self):
        return "%s: %s" % (self.chapter_name, self.chapter_desc)


class Section(models.Model):

    '''
    The ICD 10 Section and the sub-fields.
    Most fields are incorporated.
    Some fields may have been ignored.
    This is as good as the parser that was built to get the data out.

    '''

    __model_label__ = "icd10_section"

    sec_id = models.CharField(
        'Section ID', max_length=100, null=True, blank=True)
    diag_id = models.TextField(
        'Diagnosis ID', max_length=200, null=True, blank=True)
    desc = models.TextField(
        'Description', max_length=200, null=True, blank=True)
    chapter_fk = models.ForeignKey('Chapter')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s: %s" % (self.sec_id, self.diag_id)


class Diagnosis(models.Model):

    '''
    The ICD 10 Diagnosis and the sub-fields.
    Most fields are incorporated.
    Some fields may have been ignored.
    This is as good as the parser that was built to get the data out.

    '''

    __model_label__ = "icd10_diagnosis"

    diag_name = models.CharField(
        'Diagnosis Name', max_length=100, null=True, blank=True)
    diag_code = models.TextField(
        'Diagnosis Code', max_length=200, null=True, blank=True)
    section_fk = models.ForeignKey('Section')

# Define the Unicode method ::
    def __unicode__(self):
        return "%s: %s" % (self.diag_name, self.diag_code)
