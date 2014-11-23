################################################################################
# Description  : Patient Models for managing Patient Demographics & Contact 
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.settings import APP_ROOT_URL
from AuShadha.utilities.urls import UrlGenerator, generic_url_maker
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
#from patient.models import PatientDetail
PatientDetail = UI.get_module("PatientRegistration")

from dijit_fields_constants import GUARDIAN_FORM_CONSTANTS

DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES = ('patient_detail',)




class Guardian(AuShadhaBaseModel):

    """
      Class that defines the Guardian of a Particular patient.
    """

    def __init__(self, *args, **kwargs):
      super(Guardian,self).__init__(*args, **kwargs)
      self.__model_label__ = "guardian"
      self._parent_model = 'patient_detail'
    
    guardian_name = models.CharField(max_length=20, blank=True,
                                     null=True,
                                     help_text="Enter Guardian Name if Patient is a minor"
                                     )
    relation_to_guardian = models.CharField('Relation',
                                            max_length=20,
                                            blank=True,
                                            null=True,
                                            help_text="Enter relationship to Guardian if Patient is a Minor",
                                            choices=(("Father", "Father"),
                                                     ("Mother", "Mother"),
                                                     ("Local Guardian", "LocalGuardian")
                                                     )
                                            )
    guardian_phone = models.PositiveIntegerField('Phone',
                                                 max_length=20,
                                                 blank=True,
                                                 null=True
                                                 )
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)

    class Meta:
        verbose_name = "Guardian Details"
        verbose_name_plural = "Guardian Details"
        ordering = ('patient_detail', 'guardian_name')

    def __unicode__(self):
        if self.guardian_name:
            return "%s " % (self.guardian_name)
        else:
            return "No Guardian Name Provided"

############################# Model Forms ######################################

class GuardianForm(AuShadhaBaseModelForm):

    """
        ModelForm for Guardian Data Recording
    """

    __form_name__ = "Guardian Form"

    dijit_fields = GUARDIAN_FORM_CONSTANTS

    class Meta:
        model = Guardian
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES