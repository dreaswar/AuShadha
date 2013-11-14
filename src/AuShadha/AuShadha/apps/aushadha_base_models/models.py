#####################################################################################
# PROJECT      : AuShadha
# Description  : AuShadhaBaseModel and AuShadhaBaseModelForm which all models inherit
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#####################################################################################

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from django.utils import simplejson
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

import AuShadha.settings
from AuShadha.utilities.urls import generic_url_maker, UrlGenerator, urlgenerator_factory
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid


class AuShadhaBaseModel(models.Model):

    """
      Abstract Base AuShadha Model From which all AuShadha Models Derive.
    """

    def __init__(self, *args, **kwargs):
        super(AuShadhaBaseModel, self).__init__(*args, **kwargs)
        self.__model_label__ = "AuShadhaBaseModel"
        self._parent_model = None
        self.urls={}

    class Meta:
      abstract = True

    def save(self, *args, **kwargs):
        super(AuShadhaBaseModel, self).save(*args, **kwargs)
        self.generate_urls()

    def __unicode__(self):
        return unicode(self.__model_label__)

    def _generate_and_assign_urls(self,parent):
      """ Generates and Assigns URL to the Model Object"""

      #print "Printing Self:: "
      #print self
      self.urls = urlgenerator_factory(self,parent)

    def generate_urls(self):
      """ Generates and Assigns URL to the Model Object
          As of now this needs to be called as needed on instances. 

          #TODO: The result is not saved as a model attribute

          #FIXME: Calling methods on serial instances somehow replaces the self.urls in 
                  called previously. 
                  Currently it is therefore best to call it once and
                  save in a variable and use it. 
      """

      parent = getattr(self,'_parent_model',None)
      #print "Parent Instance for URL is ", parent

      if parent:
        if type(parent) is str:
          parent_field = getattr(self,parent,None)
          self._generate_and_assign_urls(parent_field)        
        elif type(parent) is list:
          for item in parent:
            p_field = getattr(self,item,None)
            if not p_field:
              continue
            else:
              self._generate_and_assign_urls(p_field)
              break
      else:
        raise Exception("NoParentModelURLError")


    def get_absolute_url(self):
        return None

    def get_formatted_obj(self):
        return None

    def get_edit_url(self):
        return generic_url_maker(self, "edit", self.id)

    def get_del_url(self):
        return generic_url_maker(self, "del", self.id)

    def get_object_json_url(self):
        return "/AuShadha/%s_json/%s/" % (self.__model_label__, self.id)

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


    #def generate_json_for_datagrid(self):
        #"""Returns the JSON formatted Values of a specific Django Model
        #Instance for use with Dojo Grid.

        #A few default DOJO Grid Values are specified, rest are instance
        #specific and are generated on the fly. It assumes the presence
        #of get_edit_url and get_del_url in the model instances passed to
        #it via obj.

        #"""
        #print "TRYING TO RETURN JSON FOR OBJECT: ", self
        #json_data = []
        #print self._meta.fields
        #data = {'add': getattr(self, 'get_add_url()', None),
                #'edit': getattr(self, 'get_edit_url()', self.get_edit_url()),
                #'del': getattr(self, 'get_del_url()', self.get_del_url()),
                #'patient_detail': getattr(self, 'patient_detail.__unicode__()', self.patient_detail.__unicode__())
                #}
        #for i in self._meta.fields:
            #print "CURRENT ITERATING FIELD NAME IS : ", i
            #print "DATA DICTIONARY NOW IS ", data.keys(), data.values()
            #if i.name not in data.keys():
                #print "Adding ", i.name
                #print i.name.__class__
                #print simplejson.dumps(i.name)
                #if i.name == "aushadhabasemodel_ptr":
                    #data[i.name] = "AuShadhaBaseModel"
                #else:
                    #data[i.name] = getattr(self, i.name, None)
##      json_data.append(data)

        #json_data = simplejson.dumps(data, cls=DjangoJSONEncoder)
        #print "RETURNED JSON IS ", unicode(json_data)
        #return json_data




class AuShadhaBaseModelForm(ModelForm):

    """
    Base class for all AuShadha ModelForms.

    Classes inheriting from this shall define two class attributes:

      1) dijit_fields : 
                      >> a dictionary of Dijit Form Fields
                      >> defaults to dijit_fields_constants.py file in same directory
                         from which the constant can be imported
                      >> Not supplying this raised a "No Dijisable Dictionary Supplied" Exception

      2) __form_name__ : 
                      >> a string describing the form


    Class Meta: attributes are the same as ModelForm
    
    __init__ Call self.generate_dijit_form which generates the Dijitised form

    """

    dijit_fields = {}

    __form_name__ = "AuShadhaBaseModelForm"

    class Meta:
        model = AuShadhaBaseModel


    def __init__(self, *args, **kwargs):
        super(AuShadhaBaseModelForm, self).__init__(*args, **kwargs)
        self.generate_dijit_form()

    def generate_dijit_form(self):
        if self.dijit_fields:
            for field_name, value_dict in self.dijit_fields.iteritems():
                for prop_key, prop_val in value_dict.iteritems():
                    self.fields[field_name].widget.attrs[prop_key] = prop_val
        else:
            print "No Text Fields ! "
            raise Exception("No Dijisable Dictionary Supplied")
