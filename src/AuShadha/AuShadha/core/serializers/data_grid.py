################################################################################
# Project     : AuShadha
# Description : Serializing methods for Dojo Datagrid
# Author      : Dr. Easwar T.R
# Date        : 25-09-2013
# License     : GNU-GPL Version 3 , See AuShadha/LICENSE.txt
################################################################################

"""
  This module and its classes used to generated Dijit DataGrid JSON

"""

#Django Imports
import json
from django.core import serializers
#from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

def generate_json_for_datagrid(obj, success=True, error_message="Saved Successfully", form_errors=None):

    """
      Returns the JSON formatted Values of a specific Django Model Instance
      for use with Dojo Grid. A few default DOJO Grid Values are specified, rest
      are instance specific and are generated on the fly. It assumes the presence
      of get_edit_url and get_del_url in the model instances passed to it via
      obj.

      ARGUMENTS: obj           : model instace / queryset
                success       : A success message
                error_message : Error Message if any.
                form_errors   : Form Validation Errors from Django while saving can be passed.

    """

    #print "TRYING TO RETURN JSON FOR OBJECT: ", obj
    json_data = []

    try:
        # Find out if the Object is an iterable one that is a Django Query Object..
        #   If iterable iterate over the fields of _meta attribute
        #   set a basic attribute dictionary and getattr method specifying
        #   default fallbacks
        iterable = iter(obj)

        if iterable:

            for element in obj:
                #print element._meta.fields
                #print "APP LABEL IS", element._meta.app_label
                data = {'success': success,
                        'error_message': unicode(error_message),
                        'form_errors': form_errors,
                        'edit': getattr(element, 'get_edit_url()', element.get_edit_url()),
                        'del': getattr(element, 'get_del_url()', element.get_del_url()),
                        'patient_detail': getattr(element, 'patient_detail.__unicode__()', None)
                        }

                for i in element._meta.fields:
                    #print "CURRENT ITERATING FIELD NAME IS : ", i
                    #print "DATA DICTIONARY NOW IS ", data.keys()

                    if i.name not in data.keys():
                        #print "Dealing with object: ", i
                        #print "Trying to add it Name attribute: ", i.name
                        #print "Class of the i object is: ", i.name.__class__

                        try:
                            if i.name == 'aushadhabasemodel_ptr':
                                data[i.name] = "AuShadhaBaseModel"
                            elif i.name == "administrator":
                                if element is not None: 
                                   data[i.name] = getattr(element, 
                                                          '__unicode__()', 
                                                          element.administrator if getattr(element,'administrator',None) else None)
                                else:
                                   data[i.name] = 'None'

                            elif i.name == "vaccine_detail":
                                if element is not None: 
                                    data[i.name] = getattr(element, '__unicode__()', element.vaccine_detail.__unicode__())
                                else:
                                    data[i.name] = 'None'
                            else:
                                data[i.name] = getattr(element, i.name, None)

                        except(TypeError):
                            raise Exception("Error In serialization..")

                json_data.append(data)

    except TypeError:
        #print obj._meta.fields
        data = {'success': success,
                'error_message': unicode(error_message),
                'form_errors': form_errors,
                'edit': getattr(obj, 'get_edit_url()', obj.get_edit_url()),
                'del': getattr(obj, 'get_del_url()', obj.get_del_url()),
                'patient_detail': getattr(obj, 'patient_detail.__unicode__()', None)
                }

        for i in obj._meta.fields:
            #print "CURRENT ITERATING FIELD NAME IS : ", i
            #print "DATA DICTIONARY NOW IS ", data.keys()

            if i.name not in data.keys():
                #print "Adding ", i.name
                #print i.name.__class__
                try:
                    if i.name == 'aushadhabasemodel_ptr':
                        data[i.name] = "AuShadhaBaseModel"
                    elif i.name == "administrator":
                        data[i.name] = getattr(
                            obj, 'username', obj.administrator.username)
                    elif i.name == "vaccine_detail":
                        data[i.name] = getattr(
                            obj, 'vaccine_name', obj.vaccine_detail.vaccine_name)
                    else:
                        data[i.name] = getattr(obj, i.name, None)

                except(TypeError):
                    raise Exception("Error In serialization..")

        json_data.append(data)

    json_data = json.dumps(json_data, cls=DjangoJSONEncoder)

#    json_serializer = serializers.get_serializer('json')()
#    json_data = json_serializer.serialize(json_data, ensure_ascii = False)
#    json_data = json.dumps(json_data)
#    print "RETURNED JSON IS ", unicode(json_data)

    return json_data
