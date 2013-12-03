################################################################################
# Description  : Patient Models for managing Patient Demographics 
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

from dijit_fields_constants import DEMOGRAPHICS_FORM_CONSTANTS
DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES = ('patient_detail',)


class Demographics(AuShadhaBaseModel):

    """
      Maintains Demographics data for the patient.
      This has been adapted from the excellent work by GNU Health project.
    """

    def __init__(self, *args, **kwargs):
      super(Demographics,self).__init__(*args, **kwargs)
      self.__model_label__ = "demographics"
      self._parent_model = 'patient_detail'

    date_of_birth = models.DateField(auto_now_add=False,
                                     null=True,
                                     blank=True
                                         )
    socioeconomics = models.CharField(max_length=100, default="Middle",
                                      choices=(("low", "Low"),
                                               ("middle", "Middle"),
                                               ("high", "High")
                                                   )
                                      )
    education = models.CharField(max_length=100,
                                 default="Graduate",
                                         choices=(('pg', 'Post-Graduate'),
                                                  ('g', 'Graduate'),
                                                  ('hs', 'High School'),
                                                  ('lg', "Lower Grade School"),
                                                  ('i', "Iliterate")
                                                  )
                                 )
    housing_conditions = models.TextField(max_length=250,
                                          default="Comfortable, with good sanitary conditions"
                                          )
    religion = models.CharField(max_length=200)
    religion_notes = models.CharField(max_length=100,
                                      null=True,
                                      blank=True
                                      )
    race = models.CharField(max_length=200)
    languages_known = models.TextField(max_length=300)
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True,
                                       unique=True
                                       )

    def __unicode__(self):
        return " Demographics for - %s" % (self.patient_detail)

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def formatted_obj_data(self):
        field_list = self._field_list()
        str_obj = "<ul>"
        for obj in field_list:
            _str = "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj




############################# Model Forms ######################################


class DemographicsForm(AuShadhaBaseModelForm):

    """
        ModelForm for Demographics Data Recording
    """

    __form_name__ = "Demographics Form"

    dijit_fields = DEMOGRAPHICS_FORM_CONSTANTS

    class Meta:
        model = Demographics
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES