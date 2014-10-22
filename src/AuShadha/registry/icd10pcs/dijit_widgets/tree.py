# -*- coding: utf-8 -*-
###############################################################
# PROJECT: AuShadha ICD10 Procedure Code Models
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################

"""
 - Axes 1..3 select a "Code Page"
 - Axis titles are specific to the "Code Page" (cv generic schema titles).
 - A "Code Page" consists of rows from axes 4..7 which match "codepage".
 - Axis titles are combined with the label info in every axis-row, so...
 - Each axis-row "title" is the same for a specific codepage, so... 
 - The first axis-row "title" can be used as the axis title. 
 
 - Axis rows, AKA "labels", have these fields...

    codepage
    code
    title
    label
"""

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


from registry.icd10pcs.models import (
    Section, 
    BodySystem, 
    Operation, 
    CodePageRow, 
    BodyPart, 
    Approach, 
    Device, 
    Qualifier, 
)


RELOAD_YAML_EACH_REQUEST = True

TREE_NODE_NAME = 'icd10pcs_tree'
CODEPAGE_NODE_NAME = 'icd10pcs_codepage'

AXIS_TARGET = (
    "<DUMMY>",
    (   Section, "ICD10PCS_CP_2_TREE"),
    (BodySystem, "ICD10PCS_CP_3_TREE"),
    ( Operation, "ICD10PCS_CP_4"),
    (  BodyPart, "<DUMMY>"),
    (  Approach, "<DUMMY>"),
    (    Device, "<DUMMY>"),
    ( Qualifier, "<DUMMY>"),
)

ROW_AXES = (BodyPart, Approach, Device, Qualifier)


yaml_filename = 'registry/icd10pcs/dijit_widgets/tree.yaml'
yaml_template = None
pane_template = None


def yaml_template_loaded(yaml_filename):
    global yaml_template
    
    if yaml_filename != None and not RELOAD_YAML_EACH_REQUEST:
        return True
        
    try:
        with open(yaml_filename, 'r') as f:
            yaml_template = f.read()
    except(IOError):
        return False
    return True
    
def pane_template_loaded(yaml_filename):
    global pane_template
    
    if not yaml_template_loaded(yaml_filename):
        return False
    if not pane_template:
        pane_template = Template(yaml_template)
    return True

def add_tree_node(node_list, node_id, node_name, widget_id):
    node_list.append({       
               'id': node_id,
             'name': node_name,
             'type': 'application',
        'widget_id': widget_id,
         'codepage': node_id,
    })
    
def create_tree_data(codepage, options, target_node, pos):
    """Create structure needed for Dijit Tree widget """
    
    tree_nodes = []
    for opt in options: 
        code = opt['code']
        cp = codepage + code
        add_tree_node(tree_nodes, cp, code+"-"+opt['label'], cp)
    
    tree_data = {
          'node_name': TREE_NODE_NAME,
           'node_obj': tree_nodes,
        'target_node': target_node,
                'pos': pos,
                'type': 'application'
    }
    return tree_data
    
def create_tree_spec(tree_data):
    rendered_pane = pane_template.render(tree_data)
    tree_spec = yaml.load(rendered_pane) 
    return tree_spec
    
def create_dijit_tree_json(tree_spec):
    widget = DijitTree()
    for node in tree_spec[TREE_NODE_NAME]:
        for k,v in node.iteritems():
            print(v)
            widget.add_child_node(DijitTreeNode(v))
    return widget.to_json()
    
    
# ABOVE: NO USE OF "REQUEST"
#-----------------------------------------------------------------------------
# BELOW: REFERENCES "REQUEST"


@login_required
def render_axis_tree(request, codepage, pos):
    """
        Called successively to construct ICD10PCS coding.
        - For pos 1..3 returns respective tree widgets (json)
        - For pos 4 returns rows for code page 
    """
    
    if not (request.method == "GET" and request.is_ajax()):
        raise Http404("Bad Request")
        
    pos = int(pos)
    if pos not in (1,2,3,4):
        raise Http404("Bad Request")
        
    # ==================================== Code Page construction
    if pos < 4: 
        
        if not pane_template_loaded(yaml_filename):
            #raise Exception("No template file to render the pane!")
            raise Http404("No template file to render the pane ! ")
        
        if codepage == '*': # Fix for yaml treating '0' as 0
            codepage = ''   # ToDo: get url to accept empty codepage
            
        axis, target_node = AXIS_TARGET[pos]
        options = axis.objects.by_codepage(codepage)
        
        tree_data = create_tree_data(codepage, options, target_node, pos+1)
        tree_data.update({
            'request': request,
            'user': request.user,
            'return_type': 'widget' if pos != 3 else 'html',
        })
        
        tree_data = RequestContext(request, tree_data)
        tree_spec = create_tree_spec(tree_data)
        
        widget_json = create_dijit_tree_json(tree_spec)
        return HttpResponse(widget_json, content_type="application/json")
            
    # ==================================== Code Page rows
    
    row_labels = []
    unique_body_parts = []

    for row in CodePageRow.objects.filter(codepage=codepage):
        row_labels.append([{
            'title': a.first().title_fk.txt, 
            'labels': a, 
            } for a in (
                row.bodypart_set.all(), 
                row.approach_set.all(), 
                row.device_set.all(), 
                row.qualifier_set.all(), 
            )
        ])
        for r in row.bodypart_set.all():
            if r.label_fk.txt not in unique_body_parts:
                unique_body_parts.append(r.label_fk.txt)

        
    codepage_rows_node = {
                 'user': request.user, 
        'codepage_rows': row_labels,
        'unique_body_parts': unique_body_parts,
    }
    variables = RequestContext(request, codepage_rows_node)
    return render_to_response('icd10pcs/codepage.html', variables)


