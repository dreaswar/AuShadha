#########################################################################
# PROJECT: AuShadha DrugBankCa Medications
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
#########################################################################

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from django.contrib.auth.models import User
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel


from AuShadha.apps.clinic.models import Clinic





class DrugBankCaDrugs(AuShadhaBaseModel):

    '''
      These models are for storing basic info from DrugbankCa
      Primary list of medications maintained would be as per FDA list
      DrugbankCa has been appended to enable drug referencing data
      Please see their website for usage terms
  
    '''

    def __init__(self, *args, **kwargs):
        super(DrugBankCaDrugs, self).__init__(*args, **kwargs)
        self.__model_label__ = "drugbank_ca_drugs"
        self._parent_model = 'parent_clinic'
        self._can_add_list_or_json = ['drugbank_ca_drugs' ]

    drug_name = models.TextField(
        'Drug Name', max_length=1000, primary_key=True)
    drug_id = models.CharField(
        'Drug-ID', max_length=30)

    # Define the Unicode method ::
    def __unicode__(self):
        return "%s - %s" % (self.drug_name, self.drug_id)

