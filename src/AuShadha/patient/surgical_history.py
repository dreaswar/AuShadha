##--------------------------------------------------------------
# Views for Patient Medical History Management
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date: 26-11-2012
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

# General Module imports-----------------------------------
from datetime import datetime, date, time



# Application Specific Model Imports-----------------------
from patient.models   import *
from admission.models import *
#from discharge.models import *
#from visit.models     import *

import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL

#from patient.surgical_history import patient_surgical_history_add, patient_surgical_history_edit
#from patient.immunisation import patient_immunisation_add, patient_immunisation_edit
#from patient.family_history import patient_family_history_add, patient_family_history_edit


from patient.views import generate_json_for_datagrid

#Views start here -----------------------------------------

@login_required
def surgical_history_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id                      = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_surgical_history_add(request, id)
    patient_detail_obj         = PatientDetail.objects.get(pk = id)
    patient_surgical_history_obj   = PatientSurgicalHistory.objects.filter(patient_detail = patient_detail_obj)
    json = generate_json_for_datagrid(patient_surgical_history_obj)
    return HttpResponse(json, content_type = "application/json")
  except(AttributeError, NameError, TypeError, ValueError, KeyError):
    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def patient_surgical_history_add(request,id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_surgical_history_obj       = PatientSurgicalHistory(patient_detail = patient_detail_obj)
        patient_surgical_history_add_form  = PatientSurgicalHistoryForm(instance = patient_surgical_history_obj)
        variable                = RequestContext(request,
                                                  {"user"                              : user,
                                                   "patient_detail_obj"                : patient_detail_obj ,
                                                   "patient_surgical_history_add_form" : patient_surgical_history_add_form,
                                                   "patient_surgical_history_obj"      : patient_surgical_history_obj ,
                                                  })
      except TypeError or ValueError or AttributeError:
       raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/surgical_history/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_surgical_history_obj       = PatientSurgicalHistory(patient_detail = patient_detail_obj)
        patient_surgical_history_add_form  = PatientSurgicalHistoryForm(request.POST,instance = patient_surgical_history_obj)
        if patient_surgical_history_add_form.is_valid():
          surgical_history_obj          = patient_surgical_history_add_form.save()
          success        = True
          error_message  = "Surgical History Data Added Successfully"
          addData        = {
                            "id"                : surgical_history_obj.id,
                            "description"       : surgical_history_obj.description,
                            "icd_10_code"       : surgical_history_obj.icd_10_code.__unicode__(),
                            "cpc_code"          : surgical_history_obj.cpc_code.__unicode__(),
                            "base_condition"    : surgical_history_obj.base_condition,
                            "med_condition"     : surgical_history_obj.med_condition.__unicode__(),
                            "classification"    : surgical_history_obj.classification,
                            "healed"            : surgical_history_obj.healed,
                            "date_of_surgery"   : surgical_history_obj.date_of_surgery.isoformat(),
                            "remarks"           : surgical_history_obj.remarks,
                            "edit"              : surgical_history_obj.get_edit_url(),
                            "del"               : surgical_history_obj.get_del_url()
          }
          data           = {'success'      : success,
                            'error_message': error_message,
                            "form_errors"  : None,
                            "addData"      : addData
          }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Surgical History data could not be added."
          form_errors   = ''
          for error in patient_surgical_history_add_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success,
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
  else:
    raise Http404("You need to Login")

@login_required
def patient_surgical_history_edit(request,id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                            = int(id)
        patient_surgical_history_obj         = PatientSurgicalHistory.objects.get(pk = id)
        patient_surgical_history_edit_form   = PatientSurgicalHistoryForm(instance = patient_surgical_history_obj)
        variable                      = RequestContext(request,
                                                  {"user"                         : user,
                                                   "patient_detail_obj"           : patient_surgical_history_obj.patient_detail ,
                                                   "patient_surgical_history_edit_form"  : patient_surgical_history_edit_form,
                                                   "patient_surgical_history_obj"        : patient_surgical_history_obj ,
                                                  })
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientSurgicalHistory.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/surgical_history/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                            = int(id)
        patient_surgical_history_obj         = PatientSurgicalHistory.objects.get(pk = id)
        patient_surgical_history_edit_form   = PatientSurgicalHistoryForm(request.POST,instance = patient_surgical_history_obj)
        if patient_surgical_history_edit_form.is_valid():
          surgical_history_obj           = patient_surgical_history_edit_form.save()
          success                 = True
          error_message           = "Surgical History Data Edited Successfully"
          addData        = {
                            "id"                : surgical_history_obj.id,
                            "description"       : surgical_history_obj.description,
                            "icd_10_code"       : surgical_history_obj.icd_10_code.__unicode__(),
                            "cpc_code"          : surgical_history_obj.cpc_code.__unicode__(),
                            "base_condition"    : surgical_history_obj.base_condition,
                            "med_condition"     : surgical_history_obj.med_condition.__unicode__(),
                            "classification"    : surgical_history_obj.classification,
                            "healed"            : surgical_history_obj.healed,
                            "date_of_surgery"   : surgical_history_obj.date_of_surgery.isoformat(),
                            "remarks"           : surgical_history_obj.remarks,
                            "edit"              : surgical_history_obj.get_edit_url(),
                            "del"               : surgical_history_obj.get_del_url()
          }
          data                    = {
                                    'success'      : success,
                                    'error_message': error_message,
                                    "form_errors"  : None,
                                    "addData"      : addData
                                    }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Surgical History data could not be added."
          form_errors   = ''
          for error in patient_surgical_history_edit_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success,
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
  else:
    raise Http404("You need to Login")

@login_required
def patient_surgical_history_del(request,id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_surgical_history_obj   = PatientSurgicalHistory.objects.get(pk = id)
          patient_detail_obj      = patient_surgical_history_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientSurgicalHistory.DoesNotExist:
          raise Http404("BadRequest: Patient surgical_history Data Does Not Exist")
       patient_surgical_history_obj.delete()
       success        = True
       error_message  = "Surgical History Data Deleted Successfully"
       data           = {'success': success, 'error_message': error_message}
       json           = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")

