# General Module imports-----------------------------------
from datetime import datetime, date, time
import yaml

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Template, Context

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree




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
      admission_node =  DijitTreeNode( y['admissions'])
      visit_node=  DijitTreeNode( y['visits'])

      #procedure_node = DijitTreeNode( y['procedures'] )
      #imaging_node = DijitTreeNode( y['imaging'] )
      #investigation_node=  DijitTreeNode( y['investigation'] )

      patient_tree_node.add_child_node( history_node )
      patient_tree_node.add_child_node( preventives_node )
      patient_tree_node.add_child_node( demographics_node )      
      patient_tree_node.add_child_node( medication_list_node )
      patient_tree_node.add_child_node( admission_node )
      patient_tree_node.add_child_node( visit_node )

      #patient_tree_node.add_child_node( procedure_node )
      #patient_tree_node.add_child_node( imaging_node )
      #patient_tree_node.add_child_node( investigation_node )

      json = patient_tree_node.to_json()
      return json