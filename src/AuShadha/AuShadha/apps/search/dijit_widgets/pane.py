################################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.template import Template, Context
from cStringIO import StringIO
import yaml
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext


from patient import MODULE_LABEL
from patient.models import PatientDetail
from AuShadha.apps.clinic.models import Clinic

@login_required
def render_aushadha_search_form(request):
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

    variable = RequestContext(request, {'user':user} )
    return render_to_response('search/search_filtering_select.html',variable)

  else:
    raise Http404("Bad Request Method") 


@login_required
def render_aushadha_search_pane(request):
  
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

      app_wrapper = []

      clinic_obj = Clinic.objects.all()

      if clinic_obj:
        clinic_id = clinic_obj[0].id
        context = Context({'clinic_id': 1 })

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
        json  = simplejson.dumps(data)

        return HttpResponse(json, content_type="application/json")

      else:
        raise Http404("No Clinic registered in AuShadha. Cannot Search! ")
 
  else:
    raise Http404("Bad Request Method") 
