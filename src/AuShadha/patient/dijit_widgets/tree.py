# General Module imports-----------------------------------
from datetime import datetime, date, time
import yaml
import json

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core import serializers
##from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder



# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree

from patient.models import PatientDetail


class PatientTree( object ):

    """
     Defines the Dijit UI for Patient Tree
    """

    def __init__(self,kwargs):

      self.request = kwargs['request']
      self.variables = RequestContext(self.request, kwargs)
      if not getattr(self.variables['patient_detail_obj'],'urls',None):
        self.variables['patient_detail_obj'].save()

      try:
        d = open('patient/dijit_widgets/tree.yaml','r')
        f = d.read()
        d.close()
        pane_template = Template( f )
        rendered_pane = pane_template.render(self.variables)
        self.yaml_file = yaml.load( rendered_pane ) 

      except( IOError ):
        raise Http404("No template file to render the pane ! ")

      try:
        self.user = self.request.user
      
      except(AttributeError,ValueError,NameError,TypeError):
        raise Exception("Invalid User or no user supplied")

    def __unicode__(self):
      return self.__call__()

    def __call__(self):

      y =  self.yaml_file
      patient_tree_node = DijitTree()
      history_node  =  DijitTreeNode( y['history'])
      preventives_node =  DijitTreeNode( y['preventives'])
      demographics_node =  DijitTreeNode( y['demographics'])
      medication_list_node =  DijitTreeNode( y['medications'])
      #admission_node =  DijitTreeNode( y['admissions'])
      visit_node=  DijitTreeNode( y['visits'])
#      icd10_node = DijitTreeNode( y['icd_10'] )
#      icd10_pcs_node = DijitTreeNode( y['icd_10_pcs'] )
#      fda_drug_db_node = DijitTreeNode( y['fda_drug_db'] )
      #procedure_node = DijitTreeNode( y['procedures'] )
      #imaging_node = DijitTreeNode( y['imaging'] )
      #investigation_node=  DijitTreeNode( y['investigation'] )
      patient_tree_node.add_child_node( history_node )
      patient_tree_node.add_child_node( preventives_node )
      patient_tree_node.add_child_node( demographics_node )      
      patient_tree_node.add_child_node( medication_list_node )
      #patient_tree_node.add_child_node( admission_node )
      patient_tree_node.add_child_node( visit_node )
#      patient_tree_node.add_child_node( icd10_node )
#      patient_tree_node.add_child_node( icd10_pcs_node )
#      patient_tree_node.add_child_node( fda_drug_db_node )
      #patient_tree_node.add_child_node( procedure_node )
      #patient_tree_node.add_child_node( imaging_node )
      #patient_tree_node.add_child_node( investigation_node )
      jsondata = patient_tree_node.to_json()
      return jsondata


@login_required
def render_patient_tree(request,patient_id = None):

  if request.method == "GET" and request.is_ajax():
    if patient_id:
      patient_id = int( patient_id )
    else:
      try:
        patient_id = int( request.GET.get('patient_id') )
      except (KeyError, NameError, ValueError,AttributeError):
        raise Http404("Bad Request: Invalid Request Parameters")
    try:
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
      if not getattr(patient_detail_obj,'urls',None):
        patient_detail_obj.save()
      d = {'request' : request,
          'patient_detail_obj': patient_detail_obj
          }
      tree = PatientTree(d)()
      print(tree)
      return HttpResponse(tree, content_type="application/json")    
    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")      
  else:
      raise Http404("Bad Request")
