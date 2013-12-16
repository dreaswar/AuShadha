################################################################################
# Project      : AuShadha
# Description  : Models for AuShadha OPD Visits.
# Author       : Dr. Easwar TR 
# Date         : 17-09-2013
# LICENSE      : GNU-GPL Version 3, Please see AuShadha/LICENSE.txt
################################################################################

# General Imports
from datetime import datetime, date, time
import importlib


# Django Specific Imports
from django.db import models
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput

# Application model imports
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm

#from AuShadha.apps.clinic.models import Clinic, Staff


VisitDetail = UI.get_module("OPD_Visit")


from dijit_fields_constants import VISIT_COMPLAINTS_FORM_CONSTANTS

DEFAULT_VISIT_COMPLAINTS_FORM_EXCLUDES = ('visit_detail',)



class VisitComplaint(AuShadhaBaseModel):
    
    def __init__(self, *args, **kwargs):
      super(VisitComplaint,self).__init__(*args, **kwargs)
      self.__model_label__ = "complaint"
      self._parent_model = 'visit_detail'

    complaint = models.CharField(max_length=30, help_text='limit to 30 words')
    duration = models.CharField(max_length=30, help_text='limit to 30 words')
    visit_detail = models.ForeignKey('visit.VisitDetail')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    #base_model = models.OneToOneField(AuShadhaBaseModel, parent_link=True)

    def __unicode__(self):
        return '%s : %s' % (self.complaint, self.duration)

    #def save(self, *args, **kwargs):
        #super(VisitComplaint, self).save(*args, **kwargs)

    # def get_edit_url(self):
        # return '/AuShadha/visit/complaint/edit/%s/' %(self.id)

    # def get_del_url(self):
        # return '/AuShadha/visit/complaint/del/%s/' %(self.id)

    class Meta:
        verbose_name = "Presenting Complaint"
        verbose_name_plural = "Presenting Complaint"
        ordering = ('visit_detail', 'created_at', 'complaint')


class VisitComplaintAddForm(AuShadhaBaseModelForm):

    __form_name__ = "Visit Complaint Form"

    dijit_fields = VISIT_COMPLAINTS_FORM_CONSTANTS


    class Meta:
        model = VisitComplaint
        exclude = ('visit_detail',)


class VisitComplaintEditForm(AuShadhaBaseModelForm):

    __form_name__ = "Visit Complaint Form"
    
    dijit_fields = VISIT_COMPLAINTS_FORM_CONSTANTS

    class Meta:
        model = VisitComplaint
        exclude = ('visit_detail',)