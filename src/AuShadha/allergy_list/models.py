##########################################################################
# PROJECT: AuShadha
#          Patient Models for managing Allergies
# Author : Dr. Easwar T R
# Date   : 16-09-2013
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
##########################################################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.apps.ui.ui import ui as UI

#from patient.models import PatientDetail
PatientDetail = UI.get_module("PatientRegistration")

from dijit_fields_constants import ALLERGY_FORM_CONSTANTS

DEFAULT_ALLERGY_FORM_EXCLUDES = ('patient_detail',)
REACTION_OBSERVED = (("rash", 'Rash'), ('angioedema',
                                        'Angioedema'), ("anaphylaxis", "Anaphylaxis"))


class Allergy(AuShadhaBaseModel):

    """
      This defines the Allergies that the patient has
    """

    def __init__(self, *args, **kwargs):
        super(Allergy, self).__init__(*args, **kwargs)
        self.__model_label__ = "allergy"
        self._parent_model = 'patient_detail'

    allergic_to = models.CharField(max_length=100)
    reaction_observed = models.CharField(max_length=100,
                                         choices=REACTION_OBSERVED,
                                         default="Rash"
                                         )
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.allergic_to)


class AllergyForm(AuShadhaBaseModelForm):

    """
      ModelForm for recording Allergies
    """

    __form_name__ = "Allergy Form"

    dijit_fields = ALLERGY_FORM_CONSTANTS

    class Meta:
        model = Allergy
        exclude = DEFAULT_ALLERGY_FORM_EXCLUDES
