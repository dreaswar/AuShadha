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
import json
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from AuShadha.apps.ui.ui import ui as UI

from registry.drug_db.drugbankca.models import DrugBankCaDrugs


@login_required
def render_drugbankcadrugs_pane(request):

  user = request.user
  if request.method == 'GET':
      app_wrapper = []
      context = RequestContext(request, {'user': user })
      try:
        pane_template = Template( 
                           open('registry/drug_db/drugbankca/dijit_widgets/pane.yaml','r').read() 
                         )
      except( IOError ):
        raise Http404("No template file to render the pane ! ")
      rendered_pane = pane_template.render(context)
      pane_yaml = yaml.load( rendered_pane ) 
      app_object = {}
      app_object['app'] = 'Drug_Bank_Ca'
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
      error_message = "Returning Drug Bank Ca app pane variables"
      data = {'success': success,
              'error_message':error_message,
              'app': app_wrapper,
              'pane': pane_yaml
              }
      jsondata = json.dumps(data)
      return HttpResponse(jsondata, content_type="application/json")
  else:
    raise Http404("Bad Request Method")
