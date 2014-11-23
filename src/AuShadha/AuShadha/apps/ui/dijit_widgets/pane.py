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
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect


from AuShadha.apps.clinic.models import Clinic
from AuShadha.apps.ui.ui import ui as UI


@login_required
def render_aushadha_ui_pane(request):
  ''' Renders the AuShadha UI '''
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

      app_wrapper = []

      clinic_obj = Clinic.objects.all()

      if clinic_obj:
        clinic_id = clinic_obj[0].id
        context = RequestContext(request, {'clinic_id': 1 , 'clinic_obj': clinic_obj ,'user': user })

        if not getattr(clinic_obj[0],'urls',None):
          print "No Attribute of URLS on Clinic. Saving to generate the same"
          clinic_obj[0].save()

        try:
          pane_template = Template( open('AuShadha/apps/ui/dijit_widgets/pane.yaml','r').read() )

        except( IOError ):
          raise Http404("No template file to render the pane ! ")

        rendered_pane = pane_template.render(context)
        pane_yaml = yaml.load( rendered_pane ) 

        #Left here as Legacy. Will be removed. 
        app_object = {}
        app_wrapper.append( app_object )

        success = True
        error_message = "Returning UI pane variables"

        data = {'success': success,'error_message':error_message,'app': app_wrapper,'pane': pane_yaml}
        jsondata  = json.dumps(data)

        return HttpResponse(jsondata, content_type="application/json")

      else:
        raise Http404("No Clinic registered in AuShadha. Cannot Search! ")
 
  else:
    raise Http404("Bad Request Method") 
