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
from django.utils import simplejson

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
MedicalHistory = UI.get_module("MedicalHistory")

from .models import VisitComplaint


# Returns True if there are no duplicates and False if there are duplicates
def check_duplicates(complaint_to_check, visit_obj):
  all_complaints = VisitComplaint.objects.filter(visit_detail = visit_obj)
  for complaint in all_complaints:

    if complaint.complaint == complaint_to_check.complaint:
      return False

  return True


@login_required
def get_all_patient_complaints(request, visit_id = None):

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

    visit_complaint_objs  = []
    all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    all_med_history = MedicalHistory.objects.filter(patient_detail  = patient_detail_obj).filter(active = True)

    for visit in all_visits:
      if visit != visit_detail_obj:
        vc = VisitComplaint.objects.filter(visit_detail = visit)
        for c in vc:
          visit_complaint_objs.append(c)

    #visit_complaint_objs = VisitComplaint.objects.filter(visit_detail = visit_detail_obj)
    data = []

    if visit_complaint_objs:
        for complaint in visit_complaint_objs:
            if not getattr(complaint, 'urls', None):
              complaint.save()
            data_to_append = {}
            data_to_append['id'] = complaint.id
            data_to_append['complaint'] = complaint.complaint
            data_to_append['duration'] = complaint.duration
            data_to_append['recorded_on'] = complaint.visit_detail.visit_date.date().isoformat()
            data_to_append['is_active'] = complaint.visit_detail.is_active
            data_to_append['edit'] = complaint.urls['edit']
            data_to_append['del'] = complaint.urls['del']
            data.append(data_to_append)

    if all_med_history:
        for medhistory in all_med_history:
            if not getattr(medhistory, 'urls', None):
              medhistory.save()
            data_to_append = {}
            data_to_append['id'] = medhistory.id
            data_to_append['complaint'] = medhistory.disease
            data_to_append['duration'] = medhistory.date_of_diagnosis.isoformat()
            data_to_append['recorded_on'] = medhistory.date_of_diagnosis.isoformat()
            data_to_append['is_active'] = True
            data_to_append['edit'] = medhistory.urls['edit']
            data_to_append['del'] = medhistory.urls['del']
            data.append(data_to_append)

    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")


@login_required
def import_active_complaints(request, visit_id = None):

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

    visit_complaint_objs  = []

    all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj).filter(is_active = True).order_by('visit_date')
    all_med_history = MedicalHistory.objects.filter(patient_detail  = patient_detail_obj).filter(active = True)
    complaint_list = [] # prevents duplication of complaints while importing

    for visit in all_visits:
      vc = VisitComplaint.objects.filter(visit_detail = visit)
      for c in vc:
            if c.complaint not in complaint_list:
                print c.complaint + " Not in list.. adding the same"
                complaint_list.append(c.complaint)

            if visit != visit_detail_obj:
                    visit_complaint_objs.append(c)

    complaint_data = []

    if visit_complaint_objs or all_med_history:

        for complaint in visit_complaint_objs:
            if complaint.complaint not in complaint_list:
                data = {'complaint': complaint.complaint,
                        'duration': complaint.duration + " ( As recorded on: " + complaint.visit_detail.visit_date.date().isoformat() + " )"
                        }
                new_complaint = VisitComplaint(**data)
                new_complaint.visit_detail = visit_detail_obj
                new_complaint.save()
                complaint_data.append({'complaint': new_complaint.complaint,
                                    'duration': new_complaint.duration,
                                    'edit' : new_complaint.urls['edit'],
                                    'del' : new_complaint.urls['del'],
                                    'id': new_complaint.id
                                    })
            else:
                continue

        for medhistory in all_med_history:
            if medhistory.disease not in complaint_list:
                data = {'complaint': medhistory.disease,
                        'duration': "From " + medhistory.date_of_diagnosis.isoformat()
                        }
                new_complaint = VisitComplaint(**data)
                new_complaint.visit_detail = visit_detail_obj
                new_complaint.save()
                complaint_data.append({'complaint': new_complaint.complaint,
                                    'duration': new_complaint.duration,
                                    'edit' : new_complaint.urls['edit'],
                                    'del' : new_complaint.urls['del'],
                                    'id': new_complaint.id
                                    })
            else:
                continue

        success = True
        error_message = "Successfully imported complaints"
        data = {'success': success, 'error_message': error_message, 'return_data': complaint_data }

    else:
        success = False
        error_message = "No Active Complaints to import..."
        data = {'success': success, 'error_message': error_message, 'return_data': complaint_data }

    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")
