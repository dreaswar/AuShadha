################################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

import yaml
from cStringIO import StringIO

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template import Template, Context
from django.contrib.auth.decorators import login_required

from AuShadha.apps.ui.ui import ui as UI
#from patient.models import PatientDetail
#from demographics.demographics.models import Demographics
#from demographics.contact.models import Contact
#from demographics.phone.models import Phone
#from demographics.guardian.models import Guardian
from demographics import MODULE_LABEL

PatientDetail = UI.get_module("PatientRegistration")
Demographics  = UI.get_module("Demographics")
Contact = UI.get_module("Contact")
Phone = UI.get_module("Phone")
Guardian = UI.get_module("Guardian")




@login_required
def render_demographics_pane(request, patient_id = None):
  
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

    try:

      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int( request.GET.get('patient_id') )

      app_wrapper = []
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
      #contact_grid_str = yaml.load( open('demographics/contact/templates/contact/dijit_widgets/grid_structures.yaml', 'r').read() )

      context = RequestContext(request, {'patient_detail_obj': patient_detail_obj})

      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()

      try:
        pane_template = Template( open('demographics/demographics/dijit_widgets/pane.yaml','r').read() )

      except( IOError ):
        raise Http404("No template file to render the pane ! ")

      rendered_pane = pane_template.render(context)
      pane_yaml = yaml.load( rendered_pane ) 
      #pane_yaml['contact_grid']['str'] = contact_grid_str

      app_object = {}
      app_object['app'] = MODULE_LABEL
      app_object['ui_sections'] = {
                                  'app_type': 'sub_module',
                                  'load_after': 'patient',
                                  'load_first': False,
                                  'layout'  :['trailing','top','center'],
                                  'widgets' :{ 'tree'    : None,
                                              'summary'  : None,
                                              'grid'     : None,
                                              'search'   : None
                                              }
                                  }
      app_object['url'] = patient_detail_obj.urls['pane']['demographics']
      app_wrapper.append( app_object )

      success = True
      error_message = "Returning "+ MODULE_LABEL + " app pane variables"

      data = {'success': success,
              'error_message':error_message,
              'app': app_wrapper,
              'pane': pane_yaml
              }
      json  = simplejson.dumps(data)

      return HttpResponse(json, content_type="application/json")

    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Bad Request Parameters")

    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")
  
  else:
    raise Http404("Bad Request Method")