################################################################################
# Description  : Patient Models for managing Patient Email and Fax
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

from dijit_fields_constants import EMAIL_AND_FAX_FORM_CONSTANTS

DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES = ('patient_detail',)



class EmailAndFax(models.Model):

    """
       Model that manages the Email, Fax and Web contact details of a patient.
    """


    def __init__(self, *args, **kwargs):
      super(EmailAndFax,self).__init__(*args, **kwargs)
      self.__model_label__ = "email_and_fax"
      self._parent_model = 'patient_detail'

    date_entered = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=75, blank=True, null=True)
    fax = models.PositiveIntegerField(
        max_length=20, null=True, blank=True)
    web = models.URLField(max_length=50, null=True, blank=True)
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)

    def __unicode__(self):
        return "%s- %s -%s" % (self.email, self.fax, self.web)

    class Meta:
        verbose_name = "Email, Web and Fax"
        verbose_name_plural = "Email, Web and Fax"
        ordering = ('date_entered', 'patient_detail')

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

class EmailAndFaxForm(AuShadhaBaseModelForm):

    """
        ModelForm for Email and Fax Data Recording
    """

    __form_name__ = "Email and Fax Form"

    dijit_fields = EMAIL_AND_FAX_FORM_CONSTANTS

    class Meta:
        model = EmailAndFax
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES
