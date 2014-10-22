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

from registry.icd10.models import Chapter, Section, Diagnosis


class ICD10Tree( object ):

    """
     Defines the Dijit UI for ICD 10 Tree
    """

    def __init__(self, *args, **kwargs):

      try:
        self.request = kwargs.get('request')
      except KeyError:
        raise Exception("ICD10 Tree Object should be initialized with a HttpRequest object at a named parameter")

      self.node_name = kwargs.get('node_name', 'chapters')
      self.yaml_path =  kwargs.get('yaml_path','registry/icd10/dijit_widgets/tree.yaml')
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
#      print y      
      for node in y[self.node_name]:
        for k, v in node.iteritems():
          c  =  DijitTreeNode( v )
          icd10_tree_node.add_child_node(c)

      jsondata = icd10_tree_node.to_json()
      return jsondata



@login_required
def render_icd10_tree(request):

  if request.method == "GET" and request.is_ajax():
      print "Received request to build ICD10 Chapter tree"
      user = request.user
      all_chapters = Chapter.objects.all()
      all_sections = Section.objects.all()
      all_diagnosis = Diagnosis.objects.all()
      d = {'request' : request,
           'user': user,
           'all_chapters': all_chapters,
           'all_sections': all_sections, 
           'all_diagnosis': all_diagnosis,
           'node_name': 'chapters'
          }
      tree = ICD10Tree(**d)()
      return HttpResponse(tree, content_type="application/json")    

  else:
      raise Http404("Bad Request")
