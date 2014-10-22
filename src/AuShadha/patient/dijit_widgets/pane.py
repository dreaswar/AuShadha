################################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

from cStringIO import StringIO
import yaml
import json

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required

from patient import MODULE_LABEL
from patient.models import PatientDetail



@login_required
def render_patient_pane(request, patient_id = None):

  user = request.user
  if request.method == 'GET' and request.is_ajax():
    try:
      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int( request.GET.get('patient_id') )
      app_wrapper = []
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
      clinic_detail_obj = patient_detail_obj.parent_clinic
      context = RequestContext(request,
                               { 'patient_detail_obj': patient_detail_obj,
                                 'patient_id': patient_id, 
                                'clinic_id': clinic_detail_obj.id 
                               })
      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()
      try:
        pane_template = Template( open('patient/dijit_widgets/pane.yaml','r').read() )
      except( IOError ):
        raise Http404("No template file to render the pane ! ")
      rendered_pane = pane_template.render(context)
      pane_yaml = yaml.load( rendered_pane ) 
      app_object = {}
      app_object['app'] = MODULE_LABEL
      app_object['ui_sections'] = {
                                  'app_type': 'main_module',
                                  'load_after': 'search',
                                  'load_first': False,
                                  'layout'  :['trailing','top','center'],
                                  'widgets' :{ 'tree'    : reverse('render_patient_tree_with_id',
                                                              kwargs= {'patient_id': patient_id} 
                                                           ),
                                              'summary'  : reverse('render_patient_summary_with_id', 
                                                              kwargs = {'patient_id': patient_id}
                                                           ),
                                              'grid'     : reverse('render_patient_json'),
                                              'search'   : reverse('render_patient_json')
                                              }
                                  }
      app_object['url'] = reverse('render_patient_tree_with_id', 
                             kwargs = {'patient_id': patient_id} 
                          )
      app_wrapper.append(app_object)
      success = True
      error_message = "Returning "+ MODULE_LABEL + " app pane variables"
      data = {'success': success,
            'error_message':error_message,
            'app': app_wrapper,
            'pane': pane_yaml
      }
      jsondata  = json.dumps(data)
      return HttpResponse(jsondata, content_type="application/json")
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Bad Request Parameters")
    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")
  else:
    raise Http404("Bad Request Method")
