################################################################################
# PROJECT     : AuShadha
# Description : Social History Models         
# Author      : Dr. Easwar T R
# Date        : 16-09-2013
# Licence     : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

import importlib

from django.db import models
#from django.forms import ModelForm
#from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm

#from patient.models import PatientDetail
from AuShadha.apps.ui.ui import ui as UI

patient = UI.registry.get('PatientRegistration','')
if patient:
  print "UI has PatientRegistration role and class defined"
  module = importlib.import_module(patient.__module__)
  PatientDetail = getattr(module, patient.__name__)
else:
  raise Exception("""
                  PatientRegistration role not defined and hence cannot be imported.
                  This module depends on this. 
                  Please register the module and class for PatientRegistration Role
                  """
                  )


from dijit_fields_constants import SOCIAL_HISTORY_FORM_CONSTANTS

DEFAULT_SOCIAL_HISTORY_FORM_EXCLUDES = ('patient_detail',)

exercise_choices = (('sendentary', "Sedentary"),
                    ("active lifestyle", "Active, but no Exercise"),
                    ("minimal", "Minimal"), ('moderate', 'Moderate'),
                    ('extreme', "Extreme")
                    )

sexual_preference_choices = (("opposite_sex", "Opposite Sex"),
                              ('same_sex', "Same Sex"),
                            ("both", "Both"),
                            ('neither', 'Neither')
                              )

marital_status_choices = (('single', "Single"),
                          ("married", "Married"),
                          ("divorced", "Divorced"),
                          ('separated', 'Separated'),
                          ('widowed', 'Widowed'),
                          ('living with partner', 'Living with Partner')
                          )

abuse_frequency = (('none', "None"), ('former', "Former"),
                    ('everyday', "Everyday"), ("periodic", "Periodic")
                    )

diet_choices = (
    ('well_balanced', "Well Balanced"),
    ('vegetarian', "Vegetarian"),
    ('jain', "Jain"),
    ('vegan', "Vegan"),
    ('non_vegetarian', "Non-Vegetarian"),
    ("junk", "Junk"),
    ("others", "Others")
)

class SocialHistory(AuShadhaBaseModel):

    """
      This defines the Social History that the patient has 
    """

    def __init__(self, *args, **kwargs):
      super(SocialHistory,self).__init__(*args, **kwargs)
      self.__model_label__ = "social_history"
      self._parent_model = 'patient_detail'


    marital_status = models.CharField(max_length=250,
                                      choices=marital_status_choices,
                                      default="Single"
                                      )
    marital_status_notes = models.CharField(max_length=250,
                                            null=True,
                                            blank=True
                                            )
    occupation = models.CharField(max_length=100)
    occupation_notes = models.CharField(max_length=100,
                                        null=True,
                                        blank=True
                                        )
    exercise = models.CharField(max_length=100,
                                choices=exercise_choices,
                                default="Active but no Exercise"
                                )
    exercise_notes = models.CharField(max_length=100,
                                      null=True,
                                      blank=True
                                      )
    diet = models.CharField(max_length=100,
                            choices=diet_choices,
                            default="Well Balanced"
                            )
    diet_notes = models.CharField(
        max_length=100, null=True, blank=True)
    home_occupants = models.CharField(max_length=300)
    home_occupants_notes = models.CharField(max_length=100,
                                            null=True,
                                            blank=True
                                            )
    pets = models.CharField(
        max_length=300, default="None")
    pets_notes = models.CharField(max_length=300,
                                  null=True,
                                  blank=True
                                  )
    alcohol = models.CharField(max_length=250,
                               choices=abuse_frequency,
                               default="None"
                               )
    alcohol_no = models.CharField(
        max_length=100, null=True, blank=True)
    alcohol_notes = models.CharField(
        max_length=250, null=True, blank=True)
    tobacco = models.CharField(max_length=250,
                               choices=abuse_frequency,
                               default="None"
                               )
    tobacco_no = models.CharField(
        max_length=250, null=True, blank=True)
    tobacco_notes = models.CharField(
        max_length=250, null=True, blank=True)
    drug_abuse = models.CharField(max_length=250,
                                  choices=abuse_frequency,
                                  default="None"
                                  )
    drug_abuse_notes = models.CharField(
        max_length=250, null=True, blank=True)
    sexual_preference = models.CharField(max_length=100,
                                         choices=sexual_preference_choices,
                                         default="Opposite Sex"
                                             )
    sexual_preference_notes = models.CharField(
        max_length=100, null=True, blank=True)
    current_events = models.TextField(max_length=300,
                                      help_text="Any ongoing / coming up issues in family having a bearing on treatment",
                                      default="None"
                                      )
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True, unique=True)

    def __unicode__(self):
        return "%s" % (self.patient_detail)



class SocialHistoryForm(AuShadhaBaseModelForm):
    """
      ModelForm for Social History
    """

    __form_name__  = "Social History Form"

    dijit_fields = SOCIAL_HISTORY_FORM_CONSTANTS

    class Meta:
        model = SocialHistory
        exclude = DEFAULT_SOCIAL_HISTORY_FORM_EXCLUDES

