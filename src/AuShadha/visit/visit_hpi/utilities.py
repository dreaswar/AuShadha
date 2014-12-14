# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
#from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator
import json

# General Module imports-----------------------------------
from datetime import datetime, date, time
#import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from collections import OrderedDict
import importlib

# Application Specific Model Imports-----------------------
from AuShadha.utilities.forms import AuModelFormErrorFormatter, aumodelformerrorformatter_factory
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.aushadha_users.models import AuShadhaUser
from AuShadha.apps.clinic.models import Clinic, Staff
from AuShadha.apps.ui.ui import ui as UI

from registry.inv_and_imaging.models import LabInvestigationRegistry, ImagingInvestigationRegistry

PatientDetail = UI.get_module("PatientRegistration")
VisitDetail  = UI.get_module("OPD_Visit")


from .models import VisitHPI


@login_required
def get_all_visit_hpi(request, visit_id = None):

    user = request.user

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))          

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()
    
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    
    except(VisitDetail.DoesNotExist):
        raise Http404("ERROR:: Visit requested does not exist.")

    visit_hpi_objs  = []
    all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    for visit in all_visits:
      if visit != visit_detail_obj:
        vc = VisitHPI.objects.filter(visit_detail = visit)
        for c in vc:
          visit_hpi_objs.append(c)

    #visit_hpi_objs = VisitHPI.objects.filter(visit_detail = visit_detail_obj)
    #data = []

    #if visit_hpi_objs:
    for hpi in visit_hpi_objs:
        if not getattr(hpi, 'urls', None):
            hpi.save()
        #data_to_append = {}
        #data_to_append['id'] = hpi.id
        #data_to_append['visit_date'] = hpi.visit_detail.visit_date.date().isoformat()
        #data_to_append['op_surgeon'] = hpi.visit_detail.op_surgeon.__unicode__()
        #data_to_append['hpi']  = hpi.hpi
        #data_to_append['edit'] = hpi.urls['edit']
        #data_to_append['del']  = hpi.urls['del']
        #data.append(data_to_append)
    variable = RequestContext(request, 
                              {'user': user, 
                               'visit_detail_obj': visit_detail_obj,
                               'visit_hpi_objs': visit_hpi_objs
                              })
    return render_to_response('visit_hpi/get_all_visit_hpi.html', variable)
    #else:
        #data.append( "No History Recorded so far" );

    #jsondata = json.dumps(data)
    #return HttpResponse(jsondata, content_type="application/json")


@login_required
def import_active_visit_hpi(request, visit_id = None):

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))          

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()
    
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    
    except(VisitDetail.DoesNotExist):
        raise Http404("ERROR:: Visit requested does not exist.")

    visit_hpi_objs  = []

    all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj).filter(is_active = True).order_by('visit_date')
    hpi_list = [] # prevents duplication of hpi while importing

    for visit in all_visits:
      if visit != visit_detail_obj:
        vc = VisitHPI.objects.filter(visit_detail = visit)
        for c in vc:
          if c.hpi not in hpi_list:
            print c.hpi + " Not in list.. adding the same"
            hpi_list.append(c.hpi)
            visit_hpi_objs.append(c)

    hpi_data = []
    if visit_hpi_objs:
        for hpi in visit_hpi_objs:
            data = {'hpi': hpi.hpi }
            new_hpi = VisitHPI(**data)
            new_hpi.visit_detail = visit_detail_obj
            new_hpi.save()
            hpi_data.append({'hpi': new_hpi.hpi, 
                             'edit' : new_hpi.urls['edit'],
                             'del' : new_hpi.urls['del'],
                             'id': new_hpi.id
                           })
        success = True
        error_message = "Successfully imported hpi"

    else:
        success = False
        error_message = "No HPI to import..."

    data = {'success': success, 'error_message': error_message, 'return_data': hpi_data }
    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type="application/json")  