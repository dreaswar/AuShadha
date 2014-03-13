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

from registry.icd10_pcs.models import PcsTable, PcsRow, BodyPart, Approach, Device, Qualifier


class ICD10PcsTree( object ):

    """
     Defines the Dijit UI for ICD 10 PCS Code Tree
    """

    def __init__(self, *args, **kwargs):

      try:
        self.request = kwargs.get('request')
      except KeyError:
        raise Exception("ICD10 PCS Tree Object should be initialized with a HttpRequest object at a named parameter")

      self.node_name = kwargs.get( 'node_name', 'pcstables' )
      self.yaml_path =  kwargs.get( 'yaml_path','registry/icd10_pcs/dijit_widgets/tree.yaml' )
      self.variables = RequestContext(self.request, kwargs)

      try:
        d = open(self.yaml_path,'r')
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
      icd10_tree_node = DijitTree()
      print y      
      for node in y[self.node_name]:
        for k, v in node.iteritems():
          c  =  DijitTreeNode( v )
          icd10_tree_node.add_child_node(c)

      json = icd10_tree_node.to_json()
      return json



@login_required
def render_icd10_pcs_tree(request,node_name = 'pcstables', parent_node_id = None):

  if request.method == "GET" and request.is_ajax():
      print "Received request to build ICD10 Pcs tree"
      user = request.user
  
      if node_name == 'pcstables':
        node_obj = PcsTable.objects.all()

      else:
        if parent_node_id:
          try:
            parent_node_id = int(parent_node_id)
            if node_name == 'pcsrows':
              parent_node_obj = PcsTable.objects.get(pk = parent_node_id)
            else:
              parent_node_obj = PcsRow.objects.get(pk  = parent_node_id)

          except (ValueError, TypeError, NameError, AttributeError):
            raise Http404("Bad Request Parameters: raises ServerErrors !")
        else:
            raise Http404("Bad Request Parameters: No Parent Node ID supplied")


        if node_name == 'pcsrows':
          node_obj = PcsRow.objects.filter(pcsTable_fk = parent_node_obj)
        elif node_name == 'devices':
          node_obj = Device.objects.filter(pcsRow_fk = parent_node_obj)
        elif node_name == 'approaches':
          node_obj = Approach.objects.filter(pcsRow_fk = parent_node_obj)
        elif node_name == 'bodyparts':
          node_obj = BodyPart.objects.filter(pcsRow_fk = parent_node_obj)
        elif node_name == 'qualifiers':
          node_obj = Qualifier.objects.filter(pcsRow_fk = parent_node_obj)
        else:
          raise Http404("Bad Request Parameters: Requested node name is not valid")

      d = {'request' : request,
           'user': user,
           'node_obj': node_obj,
           'node_name': node_name
          }
      print "*" *100
      print node_obj
      tree = ICD10PcsTree(**d)()
      return HttpResponse(tree, content_type="application/json")    

  else:
      raise Http404("Bad Request: Only GET request is accepted")
