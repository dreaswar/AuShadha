################################################################################
# Project      : AuShadha
# Description  : Models for AuShadha OPD Visits.
# Author       : Dr. Easwar TR 
# Date         : 17-09-2013
# LICENSE      : GNU-GPL Version 3, Please see AuShadha/LICENSE.txt
################################################################################

# General Imports
from datetime import datetime, date, time
import importlib


# Django Specific Imports
from django.db import models
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput

# Application model imports
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm
from AuShadha.apps.clinic.models import Clinic, Staff
from registry.inv_and_imaging.models import ImagingInvestigationRegistry, LabInvestigationRegistry
#from patient.models import PatientDetail
#from admission.models import AdmissionDetail

PatientDetail = UI.get_module("PatientRegistration")
AdmissionDetail = UI.get_module("Admission")
VisitDetail = UI.get_module("OPD_Visit")


from dijit_fields_constants import VISIT_HPI_FORM_CONSTANTS

DEFAULT_VISIT_HPI_FORM_EXCLUDES = ('patient_detail',)


class VisitHPI(AuShadhaBaseModel):
    
    def __init__(self, *args, **kwargs):
      super(VisitHPI,self).__init__(*args, **kwargs)      
      self.__model_label__ = "hpi"
      self._parent_model = 'visit_detail'
    
    hpi = models.TextField('History of Presenting Illness', max_length=1000, help_text='limit to 1000 words')
    visit_detail = models.ForeignKey('visit.VisitDetail')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s' % (self.hpi)

    def get_all_patient_hpi_url(self):
        return '/AuShadha/visit_hpi/hpi/get/%s/' %(self.visit_detail.id)

    def import_active_visit_hpi_url(self):
        return '/AuShadha/visit_hpi/hpi/import_active_visit_hpi/%s/' %(self.visit_detail.id)

    
    class Meta:
        unique_together   = ('hpi', 'visit_detail')
        verbose_name = "History of Presenting Illness"
        verbose_name_plural = "History of Presenting Illness"
        ordering = ('visit_detail', 'created_at', 'hpi')




class VisitHPIForm(AuShadhaBaseModelForm):

    __form_name__ = "Visit HPI Form"
    
    dijit_fields = VISIT_HPI_FORM_CONSTANTS

    class Meta:
        model = VisitHPI
        exclude = ('visit_detail','patient_detail')