#######################################################################################
# PROJECT      : AuShadha
# Description  : AuShadhaBaseModel and AuShadhaBaseModelForm which all models inherit
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#######################################################################################


"""

 This module houses the BaseClass for AuShadha Model and ModelForm. These inherit from 
 Django models.Model class and forms.ModelForm class respectively.

 The AuShadhaBaseModel is an abstract base class that all AuShadha apps can inherit from
 Models defined throughout the app can inherit from this class. 
 
 The AuShadhaBaseModelForm is a base class for all ModelForms which will help generate
   Dijit Form Widgets automatically. ModelForms defined throughout can inherit from it
   to autogenerate Dijit Widgets as per the dijit_fields_constants.py file definitions

"""


# Django imports

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
import json
from django.utils.safestring import mark_safe
#from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder


# AuShadha app imports

import AuShadha.settings
from AuShadha.utilities.urls import generic_url_maker, UrlGenerator, urlgenerator_factory
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid



class AuShadhaBaseModel(models.Model):

    """
      Description:
      -----------

        Abstract Base AuShadha Model From which all AuShadha Models Derive.
        This has several methods that can be inherited and used throughout.

        More specifically, the generate_urls method and the self.urls variable are
        meant to be a substitute for Django's reverse method to yield the URL for 
        a given object. This allows dictionary like querying in Django template to
        get the url for an object rather than use the {%url%} template tag. It is not
        any significant advantage. Just an attempt to make it a little simpler. 


      Attributes Defined here:
      -------------------------

        1) self.__model_label__ --> Like the __app_label__ attribute which Django sets, this
                                    sets a label for the model. Unlike the class __name__ this is
                                    just a string. 

                                    Main purpose is to allow construction of URLS for the object
                                    along with the _parent_model Attribute.


        2) self._parent_model --> Attribute that sets the parent model that the model is contained in
                                  This is almost a Zope like __contained_in__ attribute. 

                                  Aside from ForeignKey which can be used to trace a model relationship back, 
                                  this explicitly sets the container-contained relationship. 

                                  So there is no doubt which is the container model in case there are more than
                                  on ForeignKey relationship.This allows construction of URLS by the generate_urls method.


        3) self.urls --> A Dictionary that holds all the URLS for an object constructed at runtime
                          with all the possible actions on an object. This is an experimental attempt
                          to use this in place of Django's reverse method / the {% url %} template tag. 

                          The self.save() will call the self.generate_urls() and that will set the self.urls attribute.
                          This allows the dictionaly like access from template as opposed to the a little ugly 
                          {% url %} template tags with all the *args and **kwargs

                          This indirectly calls the urlgenerator_factory which does the setting of URLS as per actions
                          like 'add', 'edit', 'delete', 'json', 'summary', 'pane' etc..

                          This is far from clean / elegant as it stands now, but it works.


        4) field_list --> This Attribute helps collect the fields in the model class. It is useful for returning 
                          formatted presentation of the object from formatted_obj_data method. 

                          Eventually this method will be ported over to a separate Presentation class that
                          deals with only how an object is presented back as HTML / JSON / other formats. 
                          The HTML will include CSS inbuilt based on default values (min, max, range, True, False etc..)

                          An early attempt at this is in visit.visit_phyexam.presentation_class.py where all the 
                          exam findings are verified againts default values and appropriate CSS styles are generated
                          for HTML. This does not use template as variable comparison based on Python types are
                          difficult and range comparison does not work. This code of course can be put in views.py to help
                          generate template variables but the Class based approach for presentation seems clean. 

                          The disadvantage of this is that the Designer will have to meddle with Python code / ask the developer
                          to handle that should he change the CSS style / attributes later. For this purpose a template based 
                          approach stub has been started in the Presentation class which can be expanded later. 

    """

    def __init__(self, *args, **kwargs):
        """ 
         Class is Initialized with the attributes of __model_label__ , _parent_model, urls and field_list
        """
        super(AuShadhaBaseModel, self).__init__(*args, **kwargs)
        self.__model_label__ = "AuShadhaBaseModel"
        self._parent_model = None
        self.urls={}
        self.field_list = []

    class Meta:
      abstract = True

    def _field_list(self):
        """ Holds the model field list. """
        for f in self._meta.fields:
            self.field_list.append(f)

    def save(self, *args, **kwargs):
        """ Saves a model and sets the urls attribute"""
        super(AuShadhaBaseModel, self).save(*args, **kwargs)
        self.generate_urls()

    def __unicode__(self):
        """ Returns the unicode representation of the Model as the __model_label__ Attribute"""
        return unicode(self.__model_label__)

    def _generate_and_assign_urls(self,parent):
      """ Generates and Assigns URL to the Model Object"""
      self.urls = urlgenerator_factory(self,parent)


    def generate_urls(self):
      """ 
          Generates and Assigns URL to the Model Object
          As of now this needs to be called as needed on instances. 

          #TODO: The result is not saved as a model attribute

          #FIXME: Calling methods on serial instances somehow replaces the self.urls in 
                  called previously. Currently it is therefore best to call it once and
                  save in a variable and use it. 

                  If _parent_model is not set, it will raise an Exception
      """
      parent = getattr(self,'_parent_model',None)

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


    def get_formatted_obj(self):
        return None

    def formatted_obj_data_as_table(self):
      ''' Return formatted data as mark_safe HTML table '''

      print("Calling function to print data as table")

      table_open = "<table>"
      table_row_open = "<tr>"
      table_row_close = "</tr>"
      table_header_open = "<th>"
      table_header_close = "</th>"
      table_cell_open = "<td>"
      table_cell_close = "</td>"
      table_close = "</table>"
      
      def build_header(obj):
          _str_obj += table_row_open
          if obj.__class__.__name__ not in ['AutoField','ForeignKey']:
              _str_obj += table_header_open
              field_name = (obj.name).replace('_',' ').title()
              _str_obj += field_name
              _str_obj += table_header_close 
          _str_obj += table_row_close
          return _str_obj
        
      
      try:
        if not self.field_list:
            self._field_list()

        str_obj = ''
        str_obj += table_open
        str_obj += build_header(self.field_list[0])
        
        print(str_obj)
        
        for obj in self.field_list:
            str_obj += table_row_open
            if obj.__class__.__name__ not in ['AutoField','ForeignKey']:
              str_obj += table_cell_open
              #field_name = (obj.name).replace('_',' ').title()
              #str_obj += field_name
              #str_obj += table_header_close
              field_value = (obj.value_to_string(self)).replace('_',' ').title()

              if field_value in['',None]:
                field_value = '--'

              if field_value == True:
                field_value = "Yes"
              elif field_value == False:
                field_value = "No"

              str_obj += field_value
              str_obj += table_cell_close

              #_str = "<span> %s </span></br>" %(field_name, field_value)
              #str_obj += (_str + table_cell_close + table_row_close)

            else:
              continue
        str_obj += table_close
        print(str_obj)
        return mark_safe(str_obj)

      except (Exception) as e:
        raise e



    def formatted_obj_data(self):

      '''Return formatted data as mark_safe HTML paragraph '''

      try:
        if not self.field_list:
            self._field_list()

        str_obj = "<p>"
        for obj in self.field_list:

            if obj.__class__.__name__ not in ['AutoField','ForeignKey']:
              field_name = (obj.name).replace('_',' ').title()
              field_value = (obj.value_to_string(self)).replace('_',' ').title()

              if field_value in['',None]:
                field_value = '--'

              if field_value == True:
                field_value = "Yes"
              elif field_value == False:
                field_value = "No"

              _str = "<span> %s: %s </span></br>" %(field_name, field_value)
              str_obj += _str

            else:
              continue
        str_obj += "</p>"
        return mark_safe(str_obj)

      except (Exception) as e:
        raise e


    # Some URL methods. Not needed now as it has been replaced with the urls attribute.
    # Left here as hooks
    # The get_edit_url and get_del_url may be useful if one wants to generate urls for editing / deleting
    #   without meddling with the urls Attribute.

    def get_absolute_url(self):
        return None

    def get_edit_url(self):
        return generic_url_maker(self, "edit", self.id)

    def get_del_url(self):
        return generic_url_maker(self, "del", self.id)

    def get_object_json_url(self):
        return "/AuShadha/%s_json/%s/" % (self.__model_label__, self.id)

    @classmethod
    def get_pane_url(cls):
        return "/AuShadha/%s/%s/pane/" %(cls._meta.app_label,cls._meta.app_label)

    @classmethod
    def get_tree_url(cls):
        return "/AuShadha/%s/%s/tree/" %(cls._meta.app_label,cls._meta.app_label)




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

    dijit_fields = {} #FIXME This should be a instance variable. Realised it too late. Has to migrate it inside __init__ !!

    __form_name__ = "AuShadhaBaseModelForm"

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

    class Meta:
        model = AuShadhaBaseModel
