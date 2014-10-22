# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import json

#from django.template.loader import get_template
#from django.template import Context
#from django.core.context_processors import csrf
#from django.contrib.auth.models import User
#from django.views.decorators.csrf   import csrf_exempt
#from django.contrib.auth.views import logout
#from django.forms.models import modelformset_factory
#from django.forms.formsets import formset_factory
#from django.core.paginator import Paginator



# General Module imports-----------------------------------
from datetime import datetime, date, time
##import xhtml2pdf.pisa as pisa
#import cStringIO as StringIO
#from collections import OrderedDict
#import importlib

# Application Specific Model Imports-----------------------
from AuShadha.utilities.forms import AuModelFormErrorFormatter, aumodelformerrorformatter_factory
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.ui import ui as UI

#from AuShadha.apps.aushadha_users.models import AuShadhaUser
#from AuShadha.apps.clinic.models import Clinic, Staff
#from registry.inv_and_imaging.models import LabInvestigationRegistry, ImagingInvestigationRegistry

PatientDetail = UI.get_module("PatientRegistration")
VisitDetail  = UI.get_module("OPD_Visit")

from .models import VisitROS

ROS_FIELDS = [ 'const_symp',
               'eye_symp',
               'ent_symp',
               'cvs_symp',
               'resp_symp',
               'gi_symp',
               'gu_symp',
               'ms_symp',
               'integ_symp',
               'neuro_symp',
               'psych_symp',
               'endocr_symp',
               'immuno_symp',
               'hemat_symp'
             ]


@login_required
def get_all_visit_ros(request, visit_id = None):

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

    visit_ros_objs  = []
    all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    for visit in all_visits:
      if visit != visit_detail_obj:
        vc = VisitROS.objects.filter(visit_detail = visit)
        for c in vc:
          visit_ros_objs.append(c)

    for ros in visit_ros_objs:
        if not getattr(ros, 'urls', None):
            ros.save()

    variable = RequestContext(request, 
                              {'user': user, 
                               'visit_detail_obj': visit_detail_obj,
                               'visit_ros_objs': visit_ros_objs
                              })
    return render_to_response('visit_ros/get_all_visit_ros.html', variable)


@login_required
def import_active_visit_ros(request, visit_id = None):

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

    visit_ros_objs  = []

    all_visits = VisitDetail.objects.filter( patient_detail = patient_detail_obj ).filter(is_active = True).order_by('visit_date')

    for visit in all_visits:
      if visit != visit_detail_obj:
        vc = VisitROS.objects.filter(visit_detail = visit)
        for c in vc:
          visit_ros_objs.append(c)

    ros_data = []
    if visit_ros_objs:
        for ros in visit_ros_objs:
            data = {}
            for item in ROS_FIELDS:
                data[item] = getattr(ros, item, None)
            new_ros = VisitROS(**data)
            new_ros.visit_detail = visit_detail_obj
            new_ros.save()
            ros_data.append({'ros': data, 
                             'edit' : new_ros.urls['edit'],
                             'del' : new_ros.urls['del'],
                             'id': new_ros.id
                           })
        success = True
        error_message = "Successfully imported ros"

    else:
        success = False
        error_message = "No ROS to import..."

    data = {'success': success, 'error_message': error_message, 'return_data': ros_data }
    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type="application/json")  