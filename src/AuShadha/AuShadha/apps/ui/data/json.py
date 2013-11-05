import datetime
from django.utils import simplejson


class ModelInstanceJson(object):

    """
    Exports a Model Instance as JSON for Dijit Grid 
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


    def return_data(self):
      return self.exportable_fields

    def __call__(self):
      return self.as_json()
    
    def __unicode__(self):
      return unicode(self.__call__())

    def as_json(self):
      return simplejson.dumps(self.exportable_fields)

    def get_all_json_exportable_fields(self):
      """ 
        Gets the JSON exportable fields and its values as key, value pair
        This skips AutoField, OneToOneField type of field
      """
      for item in self.instance._meta.get_fields_with_model():
        
        if item[0].serialize:
          print item[0] , " of type ", item[0].__class__.__name__, " is JSON exportable "

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
      print "_can_add_list_or_json, Updated"