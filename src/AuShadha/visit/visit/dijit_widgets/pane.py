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

#from patient.models import PatientDetail
#from visit.visit.models import VisitDetail, VisitFollowUp
PatientDetail = UI.get_module("PatientRegistration")
VisitDetail = UI.get_module("OPD_Visit")
VisitFollowUp = UI.get_module("OPD_Visit_Followup")
from visit.visit import MODULE_LABEL





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

      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()

      context = Context({'patient_id': patient_id, 'patient_detail_obj': patient_detail_obj })

      try:
        pane_template = Template( open('visit/visit/dijit_widgets/pane.yaml','r').read() )

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

      #all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj )
      #for v in all_visits:
        #if not getattr(v, 'urls',None):
          #v.save()
          #if v.has_fu_visits():
            #for fu in v.has_fu_visits():
              #if not getattr(fu, 'urls', None):
                #fu.save()

      #active_visits = VisitDetail.objects.filter( patient_detail = patient_detail_obj ).filter( is_active = True )
      
      ##[ { active_visit:<active_visit>, fu:[<follow_ups>] } ]
      #active_visit_list = []
      #for v in active_visits:
        #dict_to_append = {'active_visit': None, 'fu': [] }
        #if not getattr(v, 'urls',None):
          #v.save()
          #dict_to_append['active_visit'] = v
          #if v.has_fu_visits():
            #for fu in v.has_fu_visits():
              #if not getattr(fu, 'urls', None):
                #fu.save()
                #dict_to_append['fu'].append(fu)
        #active_visit_list.append(dict_to_append)

      #inactive_visits = VisitDetail.objects.filter( patient_detail = patient_detail_obj ).filter( is_active = False )
      #inactive_visit_list = []
      #for v in inactive_visits:
        #dict_to_append = {'inactive_visit': None, 'fu': [] }
        #if not getattr(v, 'urls',None):
          #v.save()
          #dict_to_append['inactive_visit'] = v
          #if v.has_fu_visits():
            #for fu in v.has_fu_visits():
              #if not getattr(fu, 'urls', None):
                #fu.save()
                #dict_to_append['fu'].append(fu)
        #inactive_visit_list.append(dict_to_append)

      #context = RequestContext(request, 
                               #{'patient_detail_obj' : patient_detail_obj , 
                                #'all_visits': all_visits,
                                #'active_visits' : active_visits,
                                #'inactive_visits': inactive_visits,
                                #'user': user ,
                                #'active_visit_list': active_visit_list,
                                #'inactive_visit_list': inactive_visit_list
                                #})
      context = RequestContext(request, 
                               {'patient_detail_obj' : patient_detail_obj , 
                                'all_visits': [],
                                #'active_visits' : active_visits,
                                #'inactive_visits': inactive_visits,
                                'user': user ,
                                #'active_visit_list': active_visit_list,
                                #'inactive_visit_list': inactive_visit_list
                                })
      try:
        tree_template = Template( open('visit/visit/dijit_widgets/tree_template.yaml','r').read() )

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
