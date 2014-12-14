################################################################################
# PROJECT      : AuShadha
# Description  : visit_prescription Models
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################


import datetime
import yaml

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.clinic.models import Clinic, Staff

from .dijit_fields_constants import VISIT_PRESCRIPTION_FORM_CONSTANTS

DEFAULT_VISIT_PRESCRIPTION_FORM_EXCLUDES=('visit_detail',)

VisitDetail = UI.get_module("OPD_Visit")

# Put all Models and ModelForms below this



class VisitPrescription(AuShadhaBaseModel):

    """ Base Prescription Model for a OPD Visit """
    
    def __init__(self, *args, **kwargs):
       super(VisitPrescription, self).__init__(*args,**kwargs)
       self.__model_label__ = 'visit_prescription'
       self._parent_model = ['visit_detail']

 
    medicament = models.TextField(max_length = 100,default = '')
    indication = models.TextField(max_length = 100, 
                        default = '', blank=True,null=True)
    allow_substitution = models.BooleanField(default = False)
    print_prescription = models.BooleanField(default = False)
    dispensing_form = models.CharField(max_length = 30, default = 'Tablet')
    route = models.CharField(max_length = 30, default = 'Oral')
    start = models.DateTimeField('Treatment Start Date',auto_now = True, 
                       auto_now_add = False, blank = True,null=True)
    end = models.DateTimeField('Treatment End Date',auto_now = True, 
                       auto_now_add = False, null = True, blank = True)
    treatment_duration = models.CharField(max_length = 30, null=True, blank =True)
    dose = models.CharField(max_length = 30)
    dose_unit = models.CharField('Unit',max_length =30)
    units = models.PositiveIntegerField(max_length =3,
                       help_text="Quantity of medications to be given; \
                                  like number of tablets/ capsules")
    frequency = models.TextField(max_length = 250)
    admin_hours = models.TextField(max_length = 250)
    review = models.DateTimeField(auto_now = False, 
                       auto_now_add = False,
                       null=True,blank=True)
    refills = models.PositiveIntegerField(max_length=2,default=0)
    comment = models.TextField(max_length = 300,null=True,blank=True,default='')
    visit_detail = models.ForeignKey('visit.VisitDetail',null=True,blank=True)


    class Meta:
      verbose_name='Visit Prescription'
      verbose_name_plural = 'Visit Prescription'


# Eventually Replace text entries for fields above with auto suggestions from 
# instance data below

class Units(models.Model):
   """ Stores the Units of Medicaments """ 
   pass

class Frequency(models.Model):
    """ Stores commonly entered Frequencies for a Medicament """
    pass

class AdminHours(models.Model):
    """ Stores commonly entered Administration Hours for Medicaments """
    pass

class DispensingForms(models.Model):
    """ Stores commonly dispensed Medication forms """
    pass

class Routes(models.Model):
    pass



#ModelForms

class VisitPrescriptionForm(AuShadhaBaseModelForm):

    dijit_fields = VISIT_PRESCRIPTION_FORM_CONSTANTS

    def __init__(self, *args, **kwargs):
        self.__form_name__ = "Visit Prescription Form"
        super(VisitPrescriptionForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model = VisitPrescription
        exclude = DEFAULT_VISIT_PRESCRIPTION_FORM_EXCLUDES    
