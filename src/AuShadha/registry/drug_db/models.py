#
# PROJECT: AuShadha Medication DB. This includes separate listing for Drugs in various countries.
# Drug DB from FDA is included in FDADrugs
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


class FDADrugs(models.Model):

    '''
    The FDA Drug DB as on 26-01-2013. This is subject to change.
    This is meant mostly as an autocompleter and has not been tested.
    Please refer, test and confirm for yourself before implementation.
    '''

    __model_label__ = "fda_drugs"

    drug_name = models.CharField(
        'Drug Name', max_length=100, null=True, blank=True)
    dosage = models.CharField(
        'Dosage', max_length=100, null=True, blank=True)
    form = models.CharField(
        'Form', max_length=100, null=True, blank=True)
    active_ingredient = models.CharField(
        'Active Ingredient', max_length=100, null=True, blank=True)

    # Define the Unicode method ::
    def __unicode__(self):
        return "%s - %s, %s \t (%s)" % (self.drug_name, self.dosage, self.form, self.active_ingredient)

    class Meta:
        verbose_name = 'FDA Drugs'
        verbose_name_plural = "FDA Drugs"
        ordering = [
            'drug_name', 'active_ingredient', 'dosage', 'form']
