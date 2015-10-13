#######################################################################################
# PROJECT      : AuShadha
# Description  : ModelInstanceJson Class Module
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#######################################################################################



"""

  | Describes the ModelInstanceJson Class. This allows export of JSON.
  | Mainly used for Dojo DataGrid

  | Takes care of exporting Related ForeignKey fields.
  | Skips import of non-serializble fields
  | ModelInstanceJson class takes the instance to serialize as an argument

  | Returns the JSON when called / when as_json() instance method is called.

"""


# Imports from stdlib
import datetime

# Imports from Django
import json



class ModelInstanceJson(object):

    """
      Exports a Model Instance as JSON 
      This is used for for Dijit Grid Widget

      __init__ takes a model instance as a argument

      1) self.instance:
                     --> The model instance

      2) self.exportable_fields:
                     --> All exportble fields for the instance
                         excludes AutoField

      3) self.related_field_list:
                     --> All related ForeignKey fields for instance

      4) self.related_object_list:
                     --> All related Objects after query

      5) self.get_all_related_fields:
                     --> Gets all related fields

      6) self.get_all_json_exportable_fields:
                     --> Gets all JSON exportable fields
                         Some field types raise NotSerializable error
                         I have excluded some type, but this may not be
                         comprehensive. This will need testing.
      7) as_json: 
                --> Returns the JSON
    """

    def __init__(self,instance):
      self.model = instance.__class__
      self.instance = instance
      if not getattr(self.instance,'urls',None):
        self.instance.save()
      self.urls = self.instance.urls
      self.exportable_fields = {}
      self.related_field_list = []
      self.related_object_list = []
      self.get_all_related_fields()
      self.get_all_json_exportable_fields()

    def __call__(self):
      ''' Returns the serialized JSON when called '''
      return self.as_json()

    def __unicode__(self):
      return unicode(self.__call__())

    def return_data(self):
      ''' Returns the self.exportable_fields'''
      return self.exportable_fields

    def as_json(self):
      ''' Returns the data as a serialized JSON '''
      return json.dumps(self.exportable_fields)

    def get_all_json_exportable_fields(self):
      """ 
        Gets the JSON exportable fields and its values as key, value pair
        This skips AutoField, OneToOneField type of field
      """

      for item in self.instance._meta.get_fields_with_model():

        if item[0].serialize:

          if type( item[0].value_from_object(self.instance) ) is datetime.datetime : 
            self.exportable_fields[item[0].name] = item[0].value_from_object(self.instance).isoformat()

          elif getattr(item[0],'related', None) : 
            field_name = getattr(item[0],'name',None)
            value= getattr(self.instance, field_name,None)
            self.exportable_fields[item[0].name] = value.__unicode__()

          else:
            self.exportable_fields[item[0].name] = item[0].value_from_object(self.instance)

        else:
          continue

      self.exportable_fields['id'] = self.instance.id
      self.exportable_fields['urls'] = self.urls


    def get_all_related_fields(self):
      """ 
        Gets the related fields (basically ForeignKey) 
        These are the keys used to add / list / json/ tree/ summary stuff in related models
        This should be useful later in URL creation automagically
      """

      for item in self.instance._meta.get_all_related_objects():
          i  = '.'.join(item.name.split(':'))
          self.related_object_list.append(i)

      for item in self.related_field_list:
        if item not in self.instance._can_add_list_or_json:
          self.instance._can_add_list_or_json.append(item)
