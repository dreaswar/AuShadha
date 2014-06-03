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


class FDADrugs(AuShadhaBaseModel):

    '''
    The FDA Drug DB as on 26-01-2013. This is subject to change.
    This is meant mostly as an autocompleter and has not been tested.
    Please refer, test and confirm for yourself before implementation.
    '''

    def __init__(self, *args, **kwargs):
        super(FDADrugs, self).__init__(*args, **kwargs)
        self.__model_label__ = "fda_drug_db"
        self._parent_model = 'parent_clinic'
        self._can_add_list_or_json = ['fda_drug_db' ]

    drug_name = models.TextField(
        'Drug Name', max_length=1000, null=True, blank=True)
    dosage = models.TextField(
        'Dosage', max_length=1000, null=True, blank=True)
    form = models.TextField(
        'Form', max_length=1000, null=True, blank=True)
    active_ingredient = models.TextField(
        'Active Ingredient', max_length=1000, null=True, blank=True)

    # Define the Unicode method ::
    def __unicode__(self):
        return "%s - %s, %s \t (%s)" % (self.drug_name, self.dosage, self.form, self.active_ingredient)

    def get_absolute_url(self):
        return "%s/%s/%s" %(self._meta.app_label, self.__model_label__, self.id)

    class Meta:
        verbose_name = 'FDA Drugs'
        verbose_name_plural = "FDA Drugs"
        ordering = [ 'drug_name', 'active_ingredient', 'dosage', 'form']
