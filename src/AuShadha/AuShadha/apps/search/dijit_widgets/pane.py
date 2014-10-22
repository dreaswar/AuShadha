################################################################################
# Project: AuShadha
# Description: Pane of the Search UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

""" 
  Views to generate the UI for Search Pane
"""

# General Imports
from cStringIO import StringIO
import yaml
import json

# Django Imports
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

#AuShadha imports
from AuShadha.apps.clinic.models import Clinic
from AuShadha.apps.ui.ui import ui as UI


PatientDetail = UI.get_module("PatientRegistration")

try:
  from patient import MODULE_LABEL
except (ImportError, AttributeError):
  MODULE_LABEL = "Patient"




@login_required
def render_aushadha_search_form(request):
  '''
   Renders the AuShadha Search Form
  '''
  user = request.user
  if request.method == 'GET' and request.is_ajax():
    variable = RequestContext(request, {'user':user} )
    return render_to_response('search/search_filtering_select.html',variable)
  else:
    raise Http404("Bad Request Method") 


@login_required
def render_aushadha_search_pane(request):
  '''
    Renders the AuShadha search pane
  '''
  user = request.user
  if request.method == 'GET' and request.is_ajax():
      app_wrapper = []
      clinic_obj = Clinic.objects.all()
      if clinic_obj:
        clinic_id = clinic_obj[0].id
        context = RequestContext(request, {'clinic_id': 1 })
        if not getattr(clinic_obj[0],'urls',None):
          print "No Attribute of URLS on Clinic. Saving to generate the same"
          clinic_obj[0].save()
        try:
          pane_template = Template( open('AuShadha/apps/search/dijit_widgets/pane.yaml','r').read() )
        except( IOError ):
          raise Http404("No template file to render the pane ! ")
        rendered_pane = pane_template.render(context)
        pane_yaml = yaml.load( rendered_pane ) 
        app_object = {}
        app_object['app'] = MODULE_LABEL
        app_object['ui_sections'] = {
                                    'app_type': 'main_module',
                                    'load_after': 'first',
                                    'load_first': True,
                                    'layout'  :['trailing','top','center'],
                                    'widgets' :{ 'tree'    : None,
                                                'summary'  : None,
                                                'grid'     : reverse('aushadha_patient_search'),
                                                'search'   : reverse('aushadha_patient_search')
                                                }
                                    }
        app_object['url'] = reverse('aushadha_patient_search')
        app_wrapper.append( app_object )
        success = True
        error_message = "Returning "+ MODULE_LABEL + " app pane variables"
        data = {'success': success,'error_message':error_message,'app': app_wrapper,'pane': pane_yaml}
        jsondata  = json.dumps(data)
        return HttpResponse(jsondata, content_type="application/json")

      else:
        raise Http404("No Clinic registered in AuShadha. Cannot Search! ")
 
  else:
    raise Http404("Bad Request Method") 
