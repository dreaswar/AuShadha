################################################################################
# Project     : AuShadha
# Description : Views for Initial UI Loading
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time
import importlib

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

from django.utils import simplejson
from django.core import serializers
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic
from patient.models import PatientDetail


# Views start here -----------------------------------------


@login_required
def aushadha_patient_search(request, id= None):
  # FIXME Dojo sends REST queries with * suffix. This has to be split and dealt with before json generation is done.
  user = request.user
  if request.method == "GET" and request.is_ajax():
      if not id:
          try:
              name = unicode(request.GET.get('name'))
              print "You have queried Patients with Full Name containing: ", name
          except(TypeError, ValueError, NameError, KeyError):
              raise Http404(
                  "Bad Parameters.. No Search Results Could be returned. ")
          if name == "*":
              pat_obj = PatientDetail.objects.all()
          elif name[-1:] == "*":
              name = name[0:-1]
              print "Name after stripping trailing '*' is: ", name
              pat_obj = PatientDetail.objects.filter(
                  full_name__icontains=name)
          else:
              pat_obj = PatientDetail.objects.filter(
                  full_name__icontains=name)
          json = []
          if pat_obj:
              for patient in pat_obj:
                  data_to_append = {}
                  data_to_append['name'] = patient.full_name
                  data_to_append['id'] = patient.id
                  data_to_append['hospital_id'] = patient.patient_hospital_id
                  data_to_append['age'] = patient.age
                  data_to_append['sex'] = patient.sex
                  data_to_append['label'] = patient.full_name + "-" + \
                      patient.age       + "/" + \
                      patient.sex       + "(" + \
                      patient.patient_hospital_id + ")"
                  json.append(data_to_append)
          json = simplejson.dumps(json)
          return HttpResponse(json, content_type="application/json")
      elif id:
          try:
              id = int(id)
              pat_obj = PatientDetail.objects.get(pk=id)
          except(TypeError, KeyError, NameError, AttributeError):
              raise Http404("ERROR ! Bad Parameters. No Patients in result.")
          except(PatientDetail.DoesNotExist):
              raise Http404("ERROR! Patient Does Not Exist")
          json = return_patient_json(pat_obj)
          return HttpResponse(json, content_type="application/json")
  else:
    raise Http404("Bad Request Method")
