################################################################################
# PROJECT      : AuShadha
# Description  : Surgical History Models and ModelForm
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
#from django.forms import ModelForm
#from django.core.exceptions import ValidationError
#from django import forms
#from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm

from patient.models import PatientDetail
#from icd_10.models import ICD10
#from icd_10_pc.models import ICD10_PC
from dijit_fields_constants import SURGICAL_HISTORY_FORM_CONSTANTS

DEFAULT_SURGICAL_HISTORY_FORM_EXCLUDES = ('patient_detail',)

class SurgicalHistory(AuShadhaBaseModel):

    """
      This defines the Surgical History that the patient has had. 
    """

    __model_label__ = "surgical_history"

    _parent_model = 'patient_detail'    

    base_condition = models.TextField("Base Condition",
                                      max_length=500,
                                      null=True,
                                      blank=True
                                      )
    description = models.TextField(max_length=1000,
                                  null=True,
                                  blank=True)
    classification = models.CharField(
        max_length=200, null=True, blank=True)

    date_of_surgery = models.DateField(auto_now_add=False,
                                       null=True,
                                       blank=True
                                       )

    healed = models.BooleanField()

    remarks = models.TextField(max_length=1000,
                               help_text="Any Other Remarks",
                               default="None"
                               )

    icd_10 = models.CharField("ICD10", max_length=100, null=True, blank=True)
    icd_10_pcs = models.CharField("ICD10 PCS",max_length=100, null=True, blank=True)

    #icd_10 = models.ForeignKey("ICD10", null=True, blank=True)
    #icd_10_pcs = models.ForeignKey("ICD10 PC", null=True, blank=True)
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True,
                                       )

    def __unicode__(self):
        return "%s" % (self.patient_detail)


class SurgicalHistoryForm(AuShadhaBaseModelForm):
    """
      Sugical History ModelForm Class
    """

    __form_name__ = "Surgical History Form"

    dijit_fields = SURGICAL_HISTORY_FORM_CONSTANTS

    class Meta:
        model = SurgicalHistory
        exclude = DEFAULT_SURGICAL_HISTORY_FORM_EXCLUDES