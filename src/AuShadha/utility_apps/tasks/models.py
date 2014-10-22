################################################################################
# PROJECT      : AuShadha
# Description  : tasks Models
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

from .dijit_fields_constants import TASK_DETAIL_FORM_CONSTANTS

DEFAULT_FORM_EXCLUDES=('assigned_to',)

PRIORITY_CHOICES = ( ('high', 'High'),('normal','Normal'), ('Low', 'low') )
STATUS_CHOICES = ( ('not_started', "Not Started"),
                   ('on_going', 'On going'),
                   ('completed', 'Completed'),
                   ('cancelled', 'Cancelled'),
                   ('deferred', 'Deferred')
                 )

class TaskDetail(AuShadhaBaseModel):
    """ 
      Base class for Task entry
    """

    def __init__(self, *args, **kwargs):

       '''__init__ for this class '''

       __model_label__ = 'task_detail'
       _parent_model = 'utility'

    name = models.CharField(max_length=30, help_text = 'limit to 30 chars')
    description = models.TextField(max_length = 1000, help_text= 'limit to 1000 chars.')
    priority = models.CharField(max_length = 30, choices = PRIORITY_CHOICES)
    deadline = models.DateTimeField(auto_now = False, auto_now_add = False)
    status = models.CharField(max_length = 30, choices = STATUS_CHOICES)
    assigned_to = models.ForeignKey(User,null=True,blank=True)

    def __unicode__(self):
        return "%s %s (%s)" %(self.name, self.description, self.assigned_to)

    def is_delayed(self):
        _now = datetime.datetime.now()
        if not _now> self.deadline and self.status not in ['completed', 'cancelled', 'deferred']:
           return True
        return

    def is_active(self):
        if self.status not in ['completed', 'cancelled', 'deferred']: return True
        return


class YAMLToAuFormLoader(object):

    """ 
     Creation of a base class to deal with Django ModelForm - Dijit Form widget handling
     Dijit values for Django Form Fields can be specified as YAML and loaded
     This can be passed to AuShadhaModelForm instance later
    """ 

    def __init__(self,*args, **kwargs):
        import os
        import yaml
    
        try:
           form_fields = open( os.path.abspath(os.path.curdir)+'/utility_apps/tasks/dijit_fields_constants.yaml' )
           self.au_form_fields_dict = yaml.load(form_fields)
           self.dijit_fields = self.au_form_fields_dict
           form_fields.close()
        except(IOError) as ex:
           raise ex

    def __call__(self):
        return self.au_form_fields_dict


class TaskDetailForm(AuShadhaBaseModelForm):
    
    """
        ModelForm for Tasks Data
    """

    def __init__(self, *args, **kwargs):
       self.__form_name__ = "Task Detail Form"
       #self.dijit_fields = TASK_DETAIL_FORM_CONSTANTS
       self.dijit_fields = YAMLToAuFormLoader().__call__()['TASK_DETAIL_FORM_CONSTANTS']

    class Meta:
        model = TaskDetail
        exclude = DEFAULT_FORM_EXCLUDES
