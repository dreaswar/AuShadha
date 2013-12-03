################################################################################
# Description  : Patient Models for managing Patient Demographics & Contact 
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
#from django.contrib.auth.models import User

from AuShadha.settings import APP_ROOT_URL
from AuShadha.utilities.urls import UrlGenerator, generic_url_maker

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.apps.ui.ui import ui as UI
#from patient.models import PatientDetail

PatientDetail = UI.get_module("PatientRegistration")

from dijit_fields_constants import CONTACT_FORM_CONSTANTS
DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES = ('patient_detail',)



class Contact(AuShadhaBaseModel):

    """
      Class that defines the Contact Address of a particular patient.
    """

    def __init__(self, *args, **kwargs):
      super(Contact,self).__init__(*args, **kwargs)
      self.__model_label__ = "contact"
      self._parent_model = 'patient_detail'

    address_type = models.CharField('Type',
                                    max_length=10,
                                    choices=(("Home", "Home"),
                                             ("Office", "Office"),
                                             ("Others", "Others")
                                             ),
                                    default = "Home")
    address = models.TextField(max_length=100,
                               help_text='limit to 100 words'
                               )
    city = models.CharField(max_length=20,
                            default='Coimbatore'
                            )
    state = models.CharField(max_length=20,
                             default="Tamil Nadu"
                             )
    country = models.CharField(max_length=20,
                               default="India"
                               )
    pincode = models.PositiveIntegerField(max_length=8,
                                          null=True,
                                          blank=True
                                              )
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True
                                       )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Address"
        ordering = ('patient_detail', 'city', 'state')

    def __unicode__(self):
        if self.pincode:
            return "%s, %s, %s, %s - %s" % (self.address,
                                            self.city,
                                            self.state,
                                            self.country,
                                            self.pincode
                                            )
        else:
            return "%s, %s, %s, %s" % (self.address,
                                       self.city,
                                       self.state,
                                       self.country
                                       )

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

class ContactForm(AuShadhaBaseModelForm):

    """
        ModelForm for Contact Details Recording
    """

    __form_name__ = "Contact Form"

    dijit_fields = CONTACT_FORM_CONSTANTS

    class Meta:
        model = Contact
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES