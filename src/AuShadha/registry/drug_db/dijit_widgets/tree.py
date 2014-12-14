#############################################################
# Project: AuShadha
# Author: Dr. Easwar T.R
# Date: 11-04-2014
# License: GNU-GPL Version 3, Please see LICENSE.txt
# 
#############################################################

""" Module that defines the FDADrugDB class and methods to build the Dijit Tree """

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
##from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree

from registry.drug_db.models import FDADrugs


class DrugDBTree( object ):

    """
     Defines the Dijit UI for Drug DB
    """

    def __init__(self, *args, **kwargs):

      try:
        self.request = kwargs.get('request')
      except KeyError:
        raise Exception("DrugDB Tree Object should be initialized with a HttpRequest object at a named parameter")

      self.node_name = kwargs.get('node_name', 'fda_drug_db')
      self.yaml_path =  kwargs.get('yaml_path','registry/drug_db/dijit_widgets/tree.yaml')
      self.variables = RequestContext(self.request, kwargs)
      print("Set variables")

      try:
        d = open(self.yaml_path,'rb')
        f = d.read()
        d.close()
        print("Read and Closed the file successfully")
        tree_template = Template( f )
        print("Prepared the template")
        rendered_tree = tree_template.render(self.variables)

        with open('registry/drug_db/dijit_widgets/rendered_tree.yaml','r' ) as in_file:
           out_file.write(rendered_tree)
           out_file.close()
        
        print("Rendered with template with variables")
        self.yaml_file = yaml.load(rendered_tree)
        print("YAML FILE Loaded") 

      except( IOError ):
        raise Http404("No template file to render the tree ! ")

      try:
        self.user = self.request.user
      
      except(AttributeError,ValueError,NameError,TypeError):
        raise Exception("Invalid User or no user supplied")

    def __unicode__(self):
      return self.__call__()

    def __call__(self):

      print("Calling the __call__")
      y =  self.yaml_file
      tree = DijitTree()
      print(y)
      print("Dijit Tree Creation to begin... ")

      for node in y[self.node_name]:
        print("Iterating through the items")
        for k, v in node.iteritems():
          c  =  DijitTreeNode( v )
          tree.add_child_node(c)
          print("Added ,", c , " to Tree")

      jsondata = tree.to_json()
      
      return json



@login_required
def render_fda_drug_db_tree(request):

  if request.method == "GET" and request.is_ajax():
      print "Received request to build Drug DB tree"
      user = request.user
#      all_drugs  = FDADrugs.objects.all()
#      print("Accumulated all the FDA Drugs") 
#      print(all_drugs)
#      d = {'request' : request,
#           'user': user,
#           'node_obj': all_drugs,
#           'node_name': 'fda_drug_db'
#      }
#      tree = DrugDBTree(**d)()

      with open('registry/drug_db/dijit_widgets/rendered_tree.yaml', 'rb') as in_file:
          y = yaml.load(in_file)

          print(y)
          print("Dijit Tree Creation to begin... ")
          for node in y['fda_drug_db']:
             print("Iterating through the items")
             for k, v in node.iteritems():
                c  =  DijitTreeNode( v )
                tree.add_child_node(c)
                print("Added ,", c , " to Tree")

          json_data = tree.to_json()
               
      print("Returning JSON for Tree")
      return HttpResponse(jsondata, content_type="application/json")    

  else:
      raise Http404("Bad Request")



