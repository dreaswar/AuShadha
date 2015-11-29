##########################################################################
# Project      : AuShadha
# Description  : Medical History Models
# Author       : Dr.Easwar T.R
# Date         : 16-09-2013
# License      : GNU-GPL Version 3, Please see AuShadha/LICENSE.txt for details
##########################################################################


import importlib

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User

from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm

#from patient.models import PatientDetail
#from registry.icd10.models import Chapter

from dijit_fields_constants import MEDICAL_HISTORY_FORM_CONSTANTS
DEFAULT_MEDICAL_HISTORY_FORM_EXCLUDES = ('patient_detail',)


PatientDetail = UI.get_module('PatientRegistration')


class MedicalHistory(AuShadhaBaseModel):

    """
      This defines the Medical History that the patient has had.
    """

    def __init__(self, *args, **kwargs):
        super(MedicalHistory, self).__init__(*args, **kwargs)
        self.__model_label__ = "medical_history"
        self._parent_model = 'patient_detail'

    disease = models.CharField(max_length=100)
    status = models.TextField("Status",
                              max_length=500,
                              null=True,
                              blank=True
                              )
    severity = models.CharField(max_length=100)
    date_of_diagnosis = models.DateField(auto_now_add=False,
                                         null=True,
                                         blank=True
                                         )

    active = models.BooleanField("Active?", default=None)
    infectious_disease = models.BooleanField(default=None)
    allergic_disease = models.BooleanField(default=None)
    pregnancy_warning = models.BooleanField(default=None)

    remarks = models.TextField(max_length=1000,
                               help_text="Any Other Remarks",
                               default="None"
                               )

    icd_10 = models.CharField("ICD 10", max_length=100, null=True, blank=True)
    #icd_10 = models.ForeignKey("ICD10", null=True, blank=True)
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True,
                                       )

    def __unicode__(self):
        return "%s" % (self.patient_detail)


class MedicalHistoryForm(AuShadhaBaseModelForm):

    """
      Medical History ModelForms
    """

    __form_name__ = "Medical History Form"
    dijit_fields = MEDICAL_HISTORY_FORM_CONSTANTS

    class Meta:
        model = MedicalHistory
        exclude = DEFAULT_MEDICAL_HISTORY_FORM_EXCLUDES
