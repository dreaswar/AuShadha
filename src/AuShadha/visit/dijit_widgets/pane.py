################################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

import importlib
from cStringIO import StringIO
import yaml

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required

from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.apps.ui.ui import ui as UI

from patient.models import PatientDetail
from visit import MODULE_LABEL
from visit.models import VisitDetail

#patient = UI.registry.get('PatientRegistration','')
#if patient:
  #print "UI has PatientRegistration role and class defined"
  #module = importlib.import_module(patient.__module__)
  #PatientDetail = getattr(module, patient.__name__)
#else:
  #raise Exception("""
                  #PatientRegistration role not defined and hence cannot be imported.
                  #This module depends on this. 
                  #Please register the module and class for PatientRegistration Role
                  #"""
                  #)



@login_required
def render_visit_pane(request, patient_id = None):
  
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

    try:

      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int( request.GET.get('patient_id') )

      app_wrapper = []
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
      context = Context({'patient_id': patient_id})

      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()

      try:
        pane_template = Template( open('visit/dijit_widgets/pane.yaml','r').read() )

      except( IOError ):
        raise Http404("No template file to render the pane ! ")

      rendered_pane = pane_template.render(context)
      pane_yaml = yaml.load( rendered_pane ) 

      app_object = {}
      app_object['app'] = MODULE_LABEL
      app_object['ui_sections'] = {
                                  'app_type': 'main_module',
                                  'load_after': 'patient',
                                  'load_first': False,
                                  'layout'  :['trailing','top','center'],
                                  'widgets' :{ 'tree'    : patient_detail_obj.urls['tree']['visit'],
                                              'summary'  : patient_detail_obj.urls['summary']['visit'],
                                              'grid'     : reverse('render_visit_json_without_id'),
                                              'search'   : reverse('render_visit_json_without_id')
                                              }
                                  }
      app_object['url'] = patient_detail_obj.urls['tree']['visit']
      app_wrapper.append( app_object )

      success = True
      error_message = "Returning "+ MODULE_LABEL + " app pane variables"

      data = {'success': success,'error_message':error_message,'app': app_wrapper,'pane': pane_yaml}
      json  = simplejson.dumps(data)

      return HttpResponse(json, content_type="application/json")

    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Bad Request Parameters")

    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")
  
  else:
    raise Http404("Bad Request Method")



@login_required
def render_visit_tree(request, patient_id = None):
  
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

    try:

      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int( request.GET.get('patient_id') )

      app_wrapper = []
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()

      all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj )
      for v in all_visits:
        if not getattr(v, 'urls',None):
          v.save()
          if v.has_fu_visits():
            for fu in v.has_fu_visits():
              if not getattr(fu, 'urls', None):
                fu.save()

      active_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj ).filter(is_active = True )
      for v in active_visits:
        if not getattr(v, 'urls',None):
          v.save()
          if v.has_fu_visits():
            for fu in v.has_fu_visits():
              if not getattr(fu, 'urls', None):
                fu.save()

      inactive_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj ).filter(is_active = False )
      for v in inactive_visits:
        if not getattr(v, 'urls',None):
          v.save()
          if v.has_fu_visits():
            for fu in v.has_fu_visits():
              if not getattr(fu, 'urls', None):
                fu.save()

      context = RequestContext(request, 
                               {'patient_detail_obj' : patient_detail_obj , 
                                'all_visits': all_visits,
                                'active_visits' : active_visits,
                                'inactive_visits': inactive_visits,
                                'user': user 
                                })

      try:
        tree_template = Template( open('visit/dijit_widgets/tree_template.yaml','r').read() )

      except( IOError ):
        raise Http404("No template file to render the Tree ")

      rendered_tree = tree_template.render(context)
      tree_yaml = yaml.load( rendered_tree ) 
      success = True
      error_message  = "Visit Tree generated successfully"
      #data = {'success': success,'error_message':error_message,'tree': tree_yaml}
      json  = simplejson.dumps(tree_yaml)

      return HttpResponse(json, content_type="application/json")

    #except (TypeError, NameError, ValueError, AttributeError, KeyError):
      #raise Http404("Bad Request Parameters")

    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")
  
  else:
    raise Http404("Bad Request Method")