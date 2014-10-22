#############################################################
# Project: AuShadha
# Author: Dr. Easwar T.R
# Date: 11-04-2014
# License: GNU-GPL Version 3, Please see LICENSE.txt
# 
#############################################################

""" Module that defines methods to build the Dijit Tree for DrugBankCaDrugs class """

# General Module imports-----------------------------------
from datetime import datetime, date, time
import yaml

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Template, Context
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from registry.drug_db.drugbankca.models import DrugBankCaDrugs


class DrugBankCaDrugsTree( object ):

    """
     Defines the Dijit UI for DrugBankCaDrugs Tree
    """

    def __init__(self, *args, **kwargs):
      try:
        self.request = kwargs.get('request')
      except KeyError:
        raise Exception("DrugBankCa Tree Object should be initialized with a HttpRequest object at a named parameter")

      self.node_name = kwargs.get('node_name', 'drugbankca_drugs')
      self.yaml_path =  kwargs.get('yaml_path','registry/drug_db/drugbankca/dijit_widgets/tree.yaml')
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
        with open('registry/drug_db/drugbankca/dijit_widgets/rendered_tree.yaml','r' ) as in_file:
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
def render_drugbankcadrugs_tree(request):
    pass

