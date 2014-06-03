################################################################################
# Project      : AuShadha
# Description  : Views for Demographics
# Author       : Dr.Easwar T.R 
# Date         : 04-10-2013
# License      : GNU-GPL Version 3, See LICENSE.txt 
################################################################################

import os
import sys
from datetime import datetime, date, time

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory


from .models import RootXML, PcsTable, PcsRow, Axis, Title, Label, Definition

# Views start here -----------------------------------------

@login_required
def get_all_pcstables_json(request):
    pass

@login_required
def get_all_pcsrows_json(request):
    pass


@login_required
def get_all_bodyparts_json(request):
   pass


@login_required
def get_all_approaches_json(request):
   pass

 
@login_required
def get_all_devices_json(request):
   pass


@login_required
def get_all_qualifiers_json(request):
   pass



@login_required
def get_pcsrows_for_pcstable(request, pcstable_id):
  pass



@login_required
def get_bodyparts_for_pcsrow(request, pcsrow_id=None):
  pass


@login_required
def get_approaches_for_pcsrow(request, pcsrow_id):
  pass


@login_required
def get_devices_for_pcsrow(request, pcsrow_id):
  pass


@login_required
def get_qualifiers_for_pcsrow(request, pcsrow_id):
  pass


@login_required
def compose_icd10_pcs_code(request):
    pass

@login_required
def icd10_pcs_code_search(request):
    
    import random

    user = request.user
    search_for = request.GET.get('name')

    if request.method == 'GET':


        if search_for == '*' or search_for == ' ':
           pass
         
        else:
           search_for = search_for.split('*')[0]
           
        data = []
        #Do your stuff here
        json = simplejson.dumps(data)
        print json
        return HttpResponse(json, content_type = 'application/json')

    else:
       return Http404("Bad Request Method")


@login_required
def get_all_icd10_pcs_codes(request):
  pass



