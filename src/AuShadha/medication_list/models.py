################################################################################
# PROJECT     : AuShadha
# Description : Models to manage Medication Lists..
# Author      : Dr. Easwar T R
# Date        : 17-09-2013
# Licence     : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

import importlib

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.apps.ui.ui import ui as UI

#from patient.models import PatientDetail

PatientDetail = UI.get_module("PatientRegistration")

from dijit_fields_constants import MEDICATION_LIST_FORM_CONSTANTS

DEFAULT_MEDICATION_LIST_FORM_EXCLUDES = ('patient_detail',)


class MedicationList(AuShadhaBaseModel):

    """Inherits from the AuShadha Base Model.

    This defines the medication list that the patient is currently
    having. The patient automatically belongs to a Clinic and has some
    add, edit, del methods defined on him.

    """
    def __init__(self, *args, **kwargs):
      super(MedicationList,self).__init__(*args, **kwargs)
      self.__model_label__ = "medication_list"
      self._parent_model = 'patient_detail'

    medication = models.CharField(max_length=100,
                                  help_text="Only Generic Names.."
                                  )
    strength = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100,
                              help_text="OD, BD, TDS, QID, HS, SOS, PID etc.."
                              )
    prescription_date = models.DateField(auto_now_add=False)
    prescribed_by = models.CharField(max_length=100,
                                     choices=(("internal", "Internal"),
                                              ("external", "External")
                                                  ),
                                     default = "Internal"
                                     )
    currently_active = models.BooleanField(default=True)
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.medication)


class MedicationListForm(AuShadhaBaseModelForm):
    
    """
      Form to deal with MedicationList entries
    
    """
    __form_name__ = "Medication List Form"
    
    dijit_fields = MEDICATION_LIST_FORM_CONSTANTS

    class Meta:
        model = MedicationList
        exclude = DEFAULT_MEDICATION_LIST_FORM_EXCLUDES