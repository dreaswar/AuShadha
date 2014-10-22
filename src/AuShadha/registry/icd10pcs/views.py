# -*- coding: utf-8 -*-
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
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory


from .models import (
    Section,
    BodySystem,
    Operation,
    BodyPart,
    Approach,
    Device,
    Qualifier
)


# ==========================

def to_json(data):
    return json.dumps(data)
    
# ==========================

# Views start here -----------------------------------------

# ================== SEARCH

@login_required
def icd10pcs_code_search(request):
    import random

    user = request.user
    search_for = request.GET.get('name')

    if request.method == 'GET':
        if search_for == '*' or search_for == ' ':
            pass
        else:
            search_for = search_for.split('*')[0]
           
        data = []
        
        #----------- PERFORM SEARCH HERE ----------
        
        jsondata = to_json(data)
        #print json
        
        return HttpResponse(jsondata, content_type = 'application/json')
    
    return Http404("Bad Request Method")

