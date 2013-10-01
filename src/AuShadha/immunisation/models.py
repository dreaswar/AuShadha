################################################################################
# Project      : AuShadha
# Description  : Immunisation Models.
# Author       : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date         : 16-09-2013
################################################################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.apps.aushadha_users.models import AuShadhaUser
from patient.models import PatientDetail
from registry.vaccine_registry.models import VaccineRegistry

from dijit_fields_constants import IMMUNISATION_FORM_CONSTANTS

INJECTION_SITE_CHOICES = (("lue", "Left Upper Arm"),
                          ("rue", "Right Upper Arm"),
                          ("lb", "Left Buttock"),
                          ("rb", "Right Buttock"),
                          ("abd", "Abdomen"),
                          ("oral", "Oral")
                        )
INJECTION_ROUTE_CHOICES = (("im", "IM"),
                           ("deep_im", "Deep IM"),
                           ("iv", "Intravenous"),
                           ("sc", "Sub Cutaneous"),
                           ("oral", "Oral")
                          )

DEFAULT_IMMUNISATION_FORM_EXCLUDES = ('patient_detail','administrator',)

class Immunisation(AuShadhaBaseModel):

    """
      This defines the Immunisation that the patient has had. 
    """

    def __init__(self, *args, **kwargs):
      super(Immunisation,self).__init__(*args, **kwargs)
      self.__model_label__ = "immunisation"
      self._parent_model = 'patient_detail'    

    vaccine_detail = models.ForeignKey(VaccineRegistry)
    route = models.CharField(max_length=30,
                             choices= INJECTION_ROUTE_CHOICES,
                             default="IM"
                             )
    injection_site = models.CharField(max_length=100,
                                      choices=INJECTION_SITE_CHOICES,
                                      default="Right Upper Arm"
                                      )
    dose = models.CharField(max_length=100)
    vaccination_date = models.DateField(auto_now_add=False)
    next_due = models.DateField(auto_now_add=False)
    adverse_reaction = models.TextField(max_length=100, default="None")

    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)
    administrator = models.ForeignKey(AuShadhaUser,null=True,blank=True)


    def __unicode__(self):
        return "%s" % (self.vaccine_detail)


class ImmunisationForm(AuShadhaBaseModelForm):

    """
      This defines the Immunisation Form 
    """

    __form_name__ = "Immunisation Form"

    dijit_fields = IMMUNISATION_FORM_CONSTANTS
    
    class Meta:
      model = Immunisation
      exclude = DEFAULT_IMMUNISATION_FORM_EXCLUDES