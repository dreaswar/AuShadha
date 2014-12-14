################################################################################
# Project     : AuShadha
# Description : Views for / visit_prescription
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

import json
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic
from AuShadha.apps.ui.ui import ui as UI

from .models import VisitPrescription, VisitPrescriptionForm 
from dijit_widgets.tree import VisitPrescriptionTree

VisitDetail = UI.get_module('OPD_Visit')


# Views start here -----------------------------------------


@login_required
def visit_prescription_list(request, visit_detail_id = None):
   """ lists the prescriptions for a visit """

   try:
        if visit_detail_id: 
            visit_detail_id = int(visit_detail_id)
        else:
            try:
                visit_detail_id = int( request.GET.get('visit_detail_id') )
            except(TypeError,KeyError,NameError,ValueError):
                raise Http404("Bad Request Parameter.")
        visit_detail_obj = VisitDetail.objects.get(pk=visit_detail_id)
        visit_prescription_objs = VisitPrescription.objects.filter(visit_detail = visit_detail_obj)
        jsondata = []
        for prescription in visit_prescription_objs:
            jsondata.append(ModelInstanceJson(prescription).return_data())
        data = json.dumps(jsondata)
        print(data)
        return HttpResponse(data, content_type='application/json')

   except(ValueError,NameError,KeyError,TypeError):
       raise Http404("Bad Request Parameters")
   except(VisitDetail.DoesNotExist):
       raise Http404("Invalid Visit Request.No Visit with the ID specified exists")
   

@login_required
def visit_prescription_add(request,id = None):
  pass

@login_required
def visit_prescription_edit(request, id):
  pass

@login_required
def visit_prescription_del(request, id):
  pass

def return_visit_prescription_json( instance ,success = True):
   json_obj = ModelInstanceJson(instance)
   return json_obj()

@login_required
def render_visit_prescription_tree(request,id = None):
  pass

@login_required
def render_visit_prescription_summary(request, id=None):
  pass

@login_required
def render_visit_prescription_json(request, id = None):
  pass
