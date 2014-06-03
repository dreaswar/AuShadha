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
from django.shortcuts import render_to_response

from AuShadha.apps.ui.ui import ui as UI

from registry.icd10_pcs.models import RootXML, PcsTable, PcsRow, Axis, Label, Title, Definition

@login_required
def render_icd10_pcs_related_items(request, node_id ):
  user = request.user
  if request.method == 'GET':
     try:
       node_id = int(node_id)
       node_obj = PcsTable.objects.get(pk = node_id)
       rows_obj = PcsRow.objects.filter(pcsTable_fk = node_obj)
       
     except (AttributeError, ValueError, NameError, TypeError):
       raise Http404("Bad Request Parameters")
     
     except (PcsTable.DoesNotExist):
       raise Http404("Requested PCS code table does not exist")
    
     variable = RequestContext(request, 
                              {'user': user, 
                               'node_obj': node_obj,
                               'rows_obj': rows_obj
                              })
     return render_to_response('icd10_pcs/icd10_pcs_related_items.html', variable)

     
  else:
     raise Http404("Bad Request method")   

@login_required
def get_icd10_pcs_pane(request):
    pass


@login_required
def render_icd10_pcs_pane(request):
  
  user = request.user
  
  if request.method == 'GET':

      app_wrapper = []
      context = RequestContext(request, {'user': user })

      try:
        pane_template = Template( open('registry/icd10_pcs/dijit_widgets/pane.yaml','r').read() )

      except( IOError ):
        raise Http404("No template file to render the pane ! ")

      rendered_pane = pane_template.render(context)
      pane_yaml = yaml.load( rendered_pane ) 

      app_object = {}
      app_object['app'] = 'ICD_10_PCS'
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
      app_object['url'] = ''
      app_wrapper.append( app_object )

      success = True
      error_message = "Returning ICD10 app pane variables"

      data = {'success': success,
              'error_message':error_message,
              'app': app_wrapper,
              'pane': pane_yaml
              }
      json  = simplejson.dumps(data)

      return HttpResponse(json, content_type="application/json")

  
  else:
    raise Http404("Bad Request Method")
