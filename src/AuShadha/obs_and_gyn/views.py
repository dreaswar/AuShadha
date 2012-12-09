##--------------------------------------------------------------
# Views for Patient contact and details display and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date: 26-09-2010
##---------------------------------------------------------------

import os, sys

# General Django Imports----------------------------------

from django.shortcuts                import render_to_response
from django.http                     import Http404, HttpResponse, HttpResponseRedirect
from django.template                 import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models      import User

from django.core.urlresolvers import reverse

from django.views.decorators.csrf   import csrf_exempt
from django.views.decorators.cache  import never_cache
from django.views.decorators.csrf   import csrf_protect
from django.views.decorators.debug  import sensitive_post_parameters

from django.core.paginator           import Paginator

from django.utils                    import simplejson
from django.core                     import serializers
from django.core.serializers         import json    
from django.core.serializers.json    import DjangoJSONEncoder

from django.contrib.auth.views       import login, logout
from django.contrib.auth.decorators  import login_required
from django.contrib.auth             import REDIRECT_FIELD_NAME
from django.contrib.auth.forms       import AuthenticationForm
from django.template.response        import TemplateResponse
from django.contrib.sites.models     import get_current_site
import urlparse

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory

# General Module imports-----------------------------------
from datetime import datetime, date, time



# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL

from patient.models     import *
from obs_and_gyn.models import *
#from admission.models  import *
#from discharge.models  import *
#from visit.models      import *

from patient.views     import *


##### Obstetric History Formset##################################

ObstetricHistoryFormset = modelformset_factory(model   = ObstetricHistory, 
                                               form    = ObstetricHistoryForm,
                                               max_num = 10, 
                                               extra   = 10, 
                                               exclude = ('obstetric_detail','parent_clinic')
                          )




#Views start here -----------------------------------------

@login_required
def obstetric_history_detail_add(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      print "Received request to add Obstetric History..."
      try:
        id                        = int(id)
        patient_detail_obj        = PatientDetail.objects.get(pk =id)
        obs_and_gyn_history_obj   = ObstetricHistoryDetail.objects.filter(patient_detail = patient_detail_obj)
        if obs_and_gyn_history_obj:
          obs_and_gyn_detail_obj      = obs_and_gyn_history_obj[0]
          obs_and_gyn_detail_form     = ObstetricHistoryDetailForm(instance = obs_and_gyn_detail_obj)
          variable = {'user'                        : user, 
                      'patient_detail_obj'          : patient_detail_obj,
                      'obs_and_gyn_detail_obj'      : obs_and_gyn_detail_obj,
                      'obs_and_gyn_detail_form'     : obs_and_gyn_detail_form,
                      'button_label'                : 'Edit',
                      'action'                      : obs_and_gyn_detail_obj.get_edit_url(),
                      'canDel'                      : True,
                      "addUrl"                      : None,
                      'editUrl'                     : obs_and_gyn_detail_obj.get_edit_url(),
                      'delUrl'                      : obs_and_gyn_detail_obj.get_del_url()
                      }
        else:
          obs_and_gyn_detail_obj      = ObstetricHistoryDetail(patient_detail = patient_detail_obj)
          obs_and_gyn_detail_form     = ObstetricHistoryDetailForm(instance = obs_and_gyn_detail_obj)
          variable                        = RequestContext(request, 
                                          {"user" 									    :	user,
                                          "patient_detail_obj"			    :	patient_detail_obj ,
                                          "obs_and_gyn_detail_form"     : obs_and_gyn_detail_form, 
                                          "obs_and_gyn_detail_obj"      : obs_and_gyn_detail_obj ,
                                          'button_label'                : "Add",
                                          "action"     : patient_detail_obj.get_patient_obstetric_history_detail_add_url(),
                                          "addUrl"     : patient_detail_obj.get_patient_obstetric_history_detail_add_url(),
                                          'canDel'     : False,
                                          'editUrl'    : None,
                                          'delUrl'     : None
                                           })
        return render_to_response('patient/obs_and_gyn_history/add_or_edit_form.html', variable)
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
    elif request.method == 'POST' and request.is_ajax():
        id                          = int(id)
        patient_detail_obj          = PatientDetail.objects.get(pk =id)
        obs_and_gyn_detail_obj      = ObstetricHistoryDetail(patient_detail = patient_detail_obj)
        obs_and_gyn_detail_form     = ObstetricHistoryDetailForm(request.POST, instance = obs_and_gyn_detail_obj)
        if obs_and_gyn_detail_form.is_valid():
          obs_and_gyn_detail_obj = obs_and_gyn_detail_form.save()
          editUrl                = obs_and_gyn_detail_obj.get_edit_url()
          delUrl                 = obs_and_gyn_detail_obj.get_del_url()
          data = {"success": True, 
                  "error_message": "Saved Successfully",
                  "editUrl": editUrl, 
                  "delUrl": delUrl
          }
        else:
          data = {"success": False, "error_message": "Error!  Forms could not be saved"}
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type = "application/json")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))



@login_required
def obstetric_history_detail_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                       = int(id)
        obs_and_gyn_detail_obj   = ObstetricHistoryDetail.objects.get(pk = id)
        obs_and_gyn_detail_form  = ObstetricHistoryDetailForm(instance = obs_and_gyn_detail_obj)
        patient_detail_obj       = obs_and_gyn_detail_obj.patient_detail
        variable                 = RequestContext(request, {
                                                      "user"                    : user,
                                                      "patient_detail_obj"      : patient_detail_obj ,
                                                      "obs_and_gyn_detail_form" : obs_and_gyn_detail_form, 
                                                      "obs_and_gyn_detail_obj"  : obs_and_gyn_detail_obj ,
                                                      'action'                  : obs_and_gyn_detail_obj.get_edit_url(),
                                                      'button_label'            : "Edit",
                                                      'canDel'                  : True,
                                                      'addUrl'                  : None,
                                                      'editUrl'                 : obs_and_gyn_detail_obj.get_edit_url(),
                                                      'delUrl'                  : obs_and_gyn_detail_obj.get_del_url(),
                                   })
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except ObstetricHistoryDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Obstetric History Data Does Not Exist")
      return render_to_response('patient/obs_and_gyn_history/add_or_edit_form.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                       = int(id)
        obs_and_gyn_detail_obj   = ObstetricHistoryDetail.objects.get(pk =id)
        obs_and_gyn_detail_form  = ObstetricHistoryDetailForm(request.POST,instance = obs_and_gyn_detail_obj)
        patient_detail_obj       = obs_and_gyn_detail_obj.patient_detail
        if obs_and_gyn_detail_form.is_valid():
          obs_and_gyn_history_obj  = obs_and_gyn_detail_form.save()
          success       = True
          error_message = "Obstetric History Data Edited Successfully"
          form_errors   = ''
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors,
                   "savedObj"     : obs_and_gyn_history_obj.patient_detail.__unicode__(),
                   "editUrl"      : obs_and_gyn_history_obj.get_edit_url(),
                   "delUrl"       : obs_and_gyn_history_obj.get_del_url(),
                   'canDel'       : True,
                   "addUrl"       : None,
                 }
#          data             = generate_json_for_datagrid(obs_and_gyn_history_obj)
          json              = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Obstetric History Data data could not be added."
          form_errors   = ''
          for error in obs_and_gyn_detail_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = {'success': success, 'error_message': error_message,'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')          
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except ObstetricHistoryDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient Obstetric History Data DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. request's AJAX status was:: ", request.is_ajax())


@login_required
def obstetric_history_detail_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                       = int(id)
          obs_and_gyn_detail_obj   = ObstetricHistoryDetail.objects.get(pk = id)
          patient_detail_obj       = obs_and_gyn_detail_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except ObstetricHistoryDetail.DoesNotExist:
          raise Http404("BadRequest: Patient Obstetric History Data Does Not Exist")
       obs_and_gyn_detail_obj.delete()
       success = True
       error_message = "Obstetric History Data Deleted Successfully"
       data = {'success'        : success, 
                'error_message' : error_message, 
                'addUrl'        : patient_detail_obj.get_patient_obstetric_history_detail_add_url(),
                'canDel'        : False, 
                'editUrl'       : None, 
                'delUrl'        : None
               }
       json = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")



