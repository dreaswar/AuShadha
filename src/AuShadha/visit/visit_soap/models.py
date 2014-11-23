################################################################################
# Project      : AuShadha
# Description  : Models for AuShadha OPD VisitSOAP.
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

PatientDetail = UI.get_module("OPD_Visit")
#AdmissionDetail = UI.get_module("Admission")


from .dijit_fields_constants import VISIT_SOAP_FORM_CONSTANTS

DEFAULT_VISIT_SOAP_FORM_EXCLUDES = ('visit_detail',)



class VisitSOAP(AuShadhaBaseModel):

    """Model to describe the Visit SOAP"""
    
    def __init__(self, *args, **kwargs):
      super(VisitSOAP,self).__init__(*args, **kwargs)      
      self.__model_label__ = "visit_soap"
      self._parent_model = 'visit_detail'

    subjective = models.TextField("Subjective", 
                                    max_length=1000, 
                                    help_text="Restrict to 1000 words"
                                    )
    
    objective = models.TextField("Objective", 
                                          max_length=1000, 
                                          help_text="Restrict to 1000 words"
                                          )
    
    assessment = models.TextField("Assessment", 
                                max_length=1000, 
                                help_text="Restrict to 1000 words"
                                )
    
    
    plan = models.TextField("Plan", 
                            max_length=1000, 
                            help_text="Restrict to 1000 words"
                            )
    
    visit_detail = models.ForeignKey('visit.VisitDetail')
    
    created_at = models.DateTimeField(auto_now_add=True, 
                                      editable=False)

    def __unicode__(self):
        return '%s\n%s\n%s\n%s\n%s\nSeen On: %s' % (
            self.subjective,
            self.objective,
            self.assessment,
            self.plan,
            self.visit_detail,
            self.visit_detail.visit_date.date().isoformat()
        )




class VisitSOAPForm(AuShadhaBaseModelForm):

    __form_name__ = "Visit SOAP Form"

    dijit_fields = VISIT_SOAP_FORM_CONSTANTS

    class Meta:
        model = VisitSOAP
        exclude = ('visit_detail', 'parent_clinic', 'created_at')