################################################################################
# Project      : AuShadha
# Description  : Models for AuShadha OPD Visits ROS.
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

#from AuShadha.apps.clinic.models import Clinic, Staff
#from registry.inv_and_imaging.models import ImagingInvestigationRegistry, LabInvestigationRegistry
#from patient.models import PatientDetail
#from admission.models import AdmissionDetail
#PatientDetail = UI.get_module("PatientRegistration")
#AdmissionDetail = UI.get_module("Admission")

VisitDetail = UI.get_module("OPD_Visit")

from dijit_fields_constants import VISIT_ROS_FORM_CONSTANTS

DEFAULT_VISIT_ROS_FORM_EXCLUDES = ('patient_detail',)



class VisitROS(AuShadhaBaseModel):

    def __init__(self, *args, **kwargs):
      super(VisitROS,self).__init__(*args, **kwargs)
      self.__model_label__ = 'visit_ros'
      self._parent_model = 'visit_detail'

    const_symp = models.TextField(
        'Constitutional', max_length=500, default="Nil")
    eye_symp = models.TextField(
        'Eyes', max_length=500, default="Nil")
    ent_symp = models.TextField(
        'Ear, Nose, Throat', max_length=500, default="Nil")
    cvs_symp = models.TextField(
        'Cardiovascular', max_length=500, default="Nil")
    resp_symp = models.TextField(
        'Respiratory', max_length=500, default="Nil")
    gi_symp = models.TextField(
        'Gastrointestinal', max_length=500, default="Nil")
    gu_symp = models.TextField(
        'Genitourinary', max_length=500, default="Nil")
    ms_symp = models.TextField(
        'Musculoskeletal', max_length=500, default="Nil")
    integ_symp = models.TextField(
        'Integumentary/ Breast', max_length=500, default="Nil")
    neuro_symp = models.TextField(
        'Neurological', max_length=500, default="Nil")
    psych_symp = models.TextField(
        'Psychiatric', max_length=500, default="Nil")
    endocr_symp = models.TextField(
        'Endocrine', max_length=500, default="Nil")
    hemat_symp = models.TextField(
        'Haematological', max_length=500, default="Nil")
    immuno_symp = models.TextField(
        'Immunologic/ Allergic', max_length=500, default="Nil")

    visit_detail = models.ForeignKey('visit.VisitDetail')
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __unicode__(self):
        return '''%s \n %s \n
              %s \n %s \n %s \n 
              %s \n %s \n %s \n 
              %s \n %s \n %s \n
              %s \n %s \n %s \n %s
           ''' % (self.const_symp,
                  self.eye_symp,
                  self.ent_symp,
                  self.cvs_symp,
                  self.resp_symp,
                  self.gi_symp,
                  self.gu_symp,
                  self.ms_symp,
                  self.integ_symp,
                  self.neuro_symp,
                  self.psych_symp,
                  self.endocr_symp,
                  self.hemat_symp,
                  self.immuno_symp,
                  self.created_at.date().isoformat())

    class Meta:
        verbose_name = "Visit Review of Systems"
        verbose_name_plural = "Visit Review of Systems"





class VisitROSForm(AuShadhaBaseModelForm):

    __form_name__ = "Visit ROS Form"

    dijit_fields = VISIT_ROS_FORM_CONSTANTS

    class Meta:
        model = VisitROS
        exclude = ('visit_detail', 'parent_clinic', 'created_at')