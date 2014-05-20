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

from registry.icd10_pcs.models import RootXML, PcsTable, PcsRow, Axis, Title, Label, Definition
from registry.icd10_pcs.queries import section_list as UNIQUE_SECTION_LIST
from registry.icd10_pcs.queries import return_tables_items_by_section_name, return_tables_by_axis_name
from registry.icd10_pcs.queries import section_mapper, body_system_mapper 

class ICD10PCSTree( object ):

    """
     Defines the Dijit UI for ICD 10 PCS
    """

    def __init__(self, *args, **kwargs):

      try:
        self.request = kwargs.get('request')
      except KeyError:
        raise Exception("ICD10 Tree Object should be initialized with a HttpRequest object at a named parameter")

      self.node_name = kwargs.get('node_name', 'pcs_tables')
      self.yaml_path =  kwargs.get('yaml_path','registry/icd10_pcs/dijit_widgets/tree.yaml')
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
      icd10_pcs_tree_node = DijitTree()

      for node in y[self.node_name]:
        for k, v in node.iteritems():
          c  =  DijitTreeNode( v )
          icd10_pcs_tree_node.add_child_node(c)

      json = icd10_pcs_tree_node.to_json()
      return json



@login_required
def render_icd10_pcs_tree(request):

  if request.method == "GET" and request.is_ajax():
      print "Received request to build ICD10 Chapter tree"
      user = request.user
      all_pcs_tables = PcsTable.objects.all()
      d = {'request' : request,
           'user': user,
           'node_obj': all_pcs_tables,
           'node_name': 'pcs_tables'
      }
      tree = ICD10PCSTree(**d)()
      return HttpResponse(tree, content_type="application/json")    

  else:
      raise Http404("Bad Request")


@login_required
def render_all_section_tree(request):
    
    """ Renders all sections as Dijit Tree widget """
    
    if request.method == 'GET' and request.is_ajax():
       user = request.user
       global UNIQUE_SECTION_LIST
       section_dict_list = []
       for item in UNIQUE_SECTION_LIST:
          if item['name'] is None: item['name'] = 'None'
          section_dict_list.append({'id': item['name'].replace(' ' ,'_').replace(',',''),
                                   'name': item['code'] + "-" + item['name'],
                                   'widget_id': item['name'].replace(' ','_')
                                  })
       print(section_dict_list)
       d = {'request': request, 
            'user': user,
            'node_obj': section_dict_list,
            'node_name': 'section_list'
       }
       tree = ICD10PCSTree(**d)()
       return HttpResponse(tree, content_type="application/json")
    else:
       raise Http404("Invalid Request Method")



@login_required
def render_per_section_body_system_tree(request, section):
   
    """ Renders body system list as Dijit Tree. This is filtered per section name"""

    section_name = section.replace('_', ' ')

    if request.method == 'GET' and request.is_ajax():
       user = request.user
       body_systems = []
       for b in section_mapper[section_name]['body_system']:
           body_systems.append({'widget_id': b[0].pk, 
                                'id': b[0].pk, 
                                'name': b[0].code +"-"+ b[0].text, 
                                'section': b[0].fk.pcsTable_fk.get_section_name()})
       d = {'request': request, 
            'user': user,
            'node_obj': body_systems,
            'node_name': 'body_system'
       }
       tree = ICD10PCSTree(**d)()
       return HttpResponse(tree, content_type="application/json")

    else:
       raise Http404("Invalid Request Method")



@login_required
def render_per_body_system_operation_tree(request,body_system):
    
    """ Renders operation list as Dijit Tree. This is filtered per Body System Name"""

    if request.method == 'GET' and request.is_ajax():
       user = request.user
       try:
         body_system_id = int(body_system)
         body_system_obj = Label.objects.get(pk= body_system_id)
         body_system = body_system_obj.fk.pcsTable_fk.get_body_system_name()
         sec = body_system_obj.fk.pcsTable_fk.get_section_name()

       except(Label.DoesNotExist):
         raise Http404("Bad Request: Invalid object request")
      
       except(ValueError,TypeError,NameError):
          raise Http404("Bad Request: Invalid Request Parameters")

       operations = []

       for o in body_system_mapper[sec][body_system]['operation']:
           operations.append({'widget_id': o.pk, 
                              'id': o.pk, 
                              'name': o.code + "-" + o.text, 
                              'section':sec })
       d = {'request': request, 
            'user': user,
            'node_obj': operations,
            'node_name': 'operation'
       }
       tree = ICD10PCSTree(**d)()
       return HttpResponse(tree, content_type="application/json")

    else:
       raise Http404("Invalid Request Method")


@login_required
def render_per_operation_pcs_row(request, operation):

  if request.method == 'GET':
      try:
        operation_id = int(operation)
        operation_obj = Label.objects.get(pk = operation_id)
        table_obj = operation_obj.fk.pcsTable_fk
        all_pcs_rows = PcsRow.objects.filter(fk = table_obj)      

      except (ValueError,NameError,TypeError):
          raise Http404 ("Bad Request Parameters")

      except (Label.DoesNotExist):
          raise Http404 ("Label Object Does not Exist! ")    

      variable = RequestContext(request, {'user': request.user, 
                                        'pcs_rows': all_pcs_rows,
                                        'operation_obj': operation_obj,
                                        'table_obj': table_obj})
      return render_to_response('icd10_pcs/pcs_row.html', variable)

  else:
      raise Http404("Bad Request Method")

@login_required
def render_pcs_rows_for_pcs_table(request,pcs_table_id):

    """" Render PCS Row Dijit Tree with all the residual code for a PcsTable"""

    pass


