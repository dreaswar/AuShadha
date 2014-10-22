# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
#from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.contrib.auth.models import User

import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
#from AuShadha.settings import APP_ROOT_URL
#from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.apps.ui.ui import ui as UI

PatientDetail = UI.get_module("PatientRegistration")
AdmissionDetail = UI.get_module("Admission")

try:
  from admission import MODULE_LABEL
except (AttributeError, ImportError):
  MODULE_LABEL = "Admission"

#from patient.models import PatientDetail
#from admission.models import AdmissionDetail


@login_required
def render_admission_pane(request, patient_id = None):
  
  user = request.user

  if request.method == 'GET' and request.is_ajax():

    #try:

      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int( request.GET.get('patient_id') )

      app_wrapper = []
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)

      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()

      app_object = {}
      app_object['app'] = MODULE_LABEL
      app_object['ui_sections'] = {
                                  'app_type': 'main_module',
                                  'load_after': 'patient',
                                  'load_first': False,
                                  'layout'  :['trailing','top','center'],
                                  'widgets' :{ 'tree'    : patient_detail_obj.urls['tree']['admission'],
                                              'summary'  : patient_detail_obj.urls['summary']['admission'],
                                              'grid'     : reverse('render_admission_json_without_id'),
                                              'search'   : reverse('render_admission_json_without_id')
                                              }
                                 }
      app_object['url'] = patient_detail_obj.urls['tree']['admission']
      app_wrapper.append( app_object )

      success = True
      error_message = "Returning "+ MODULE_LABEL + " app pane variables"

      data = {'success': success,'error_message':error_message,'app': app_wrapper}
      jsondata = json.dumps(data)

      return HttpResponse(jsondata, content_type="application/json")

    #except (TypeError, NameError, ValueError, AttributeError, KeyError):
      #raise Http404("Bad Request Parameters")

    #except (PatientDetail.DoesNotExist):
      #raise Http404("Bad Request: Patient Does Not Exist")
  
  else:
    raise Http404("Bad Request Method")