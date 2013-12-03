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

from dijit_fields_constants import PHONE_FORM_CONSTANTS

DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES = ('patient_detail',)



class Phone(AuShadhaBaseModel):

    """
      Class that defines the Phone data of a patient.
    """

    def __init__(self, *args, **kwargs):
      super(Phone,self).__init__(*args, **kwargs)
      self.__model_label__ = "phone"
      self._parent_model = 'patient_detail'

    phone_type = models.CharField('Type',
                                  max_length=10,
                                  choices=(("Home", "Home"),
                                           ("Office", "Office"),
                                           ("Mobile", "Mobile"),
                                           ("Fax", "Fax"),
                                           ("Others", "Others")
                                           ),
                                  default = "Home")
    ISD_Code = models.PositiveIntegerField('ISD',
                                           max_length=4,
                                           null=True,
                                           blank=True,
                                           default="0091"
                                           )
    STD_Code = models.PositiveIntegerField('STD',
                                           max_length=4,
                                           null=True,
                                           blank=True,
                                           default="0422"
                                           )
    phone = models.PositiveIntegerField(max_length=10,
                                        null=True,
                                        blank=True
                                        )
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True
                                       )

    class Meta:
        verbose_name = "Phone"
        verbose_name_plural = "Phone"
        ordering = ('patient_detail',
                    'phone_type',
                    'ISD_Code',
                    'STD_Code'
                    )

    def __unicode__(self):
        if self.phone:
            return "%s- %s -%s" % (self.ISD_Code, self.STD_Code, self.phone)
        else:
            return "No Phone Number Provided"

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj
############################# Model Forms ######################################


class PhoneForm(AuShadhaBaseModelForm):

    """
        ModelForm for Phone Recording
    """

    __form_name__ = "Phone Form"

    dijit_fields = PHONE_FORM_CONSTANTS

    class Meta:
        model = Phone
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES
