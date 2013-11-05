################################################################################
# Project     :
# Description :
# Author      : 
# License     :
################################################################################

import importlib
import re
from django.utils import simplejson
from .json import ModelInstanceJson




class ModelInstanceSummary(object):
  
  """
   
   Returns a summary of the model instance along with its related models
   
  """


  def __init__(self,instance,template=None):

    self.instance = instance
    self.summary_template = '%s/summary.html' %(self.instance.__model_label__)    
    j = ModelInstanceJson(self.instance)
    self.related_model_paths = j.related_object_list
    self.module_path_map = []
    self.build_module_path_map()
    self.build_variable()
    

  def __call__(self):
    return self.variable


  def __unicode__(self):
    return unicode( self.__call__() )


  def build_module_path_map(self):

      for x in self.instance._meta.get_all_related_objects():

        d = { 'module_path' : [x.model.__module__, x.model.__name__], 
             'field_name' : x.field.name 
             }
        self.module_path_map.append(d)

      self._extend_module_path_map()


  def _extend_module_path_map(self):

    for module in self.module_path_map:

        try:
          m = importlib.import_module(module['module_path'][0])
          l = re.findall('[A-Z][^A-Z]*',module['module_path'][1])
          label = ( '_'.join(l) ).lower()

          cl = getattr(m,module['module_path'][1])
          d = {module['field_name'] : self.instance}
          rel_objs = cl.objects.filter(**d)

          module['rel_objs']= {}
          module['rel_objs']['model_label'] = label
          module['rel_objs']['queryset'] = rel_objs
          #print d
          #print rel_objs

        except(ImportError):
          raise Exception("ImportError")

  def build_variable(self):
    
    l = re.findall('[A-Z][^A-Z]*',self.instance.__class__.__name__)
    label = ( '_'.join(l) ).lower() + "_obj"
    self.variable = {label: self.instance}
    
    for item in self.module_path_map:
      rel_objs = item['rel_objs']
      model_label  = rel_objs['model_label']
      queryset_name = "%s_obj" %(model_label)
      queryset = rel_objs['queryset']
      self.variable[queryset_name] = queryset


def main():
  from patient.models import PatientDetail
  from demographics.contact.models import Contact
  p = PatientDetail.objects.get(pk = 1)
  c = Contact(address_type = 'home',address="sds")
  c.patient_detail = p
  c.save()
  d = ModelInstanceSummary(p)
  return d

#main()