# --------------------------------------------------------------
# Views for Patient Medication List as part of AuShadha Project
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Please see AuShadha Project License for Details
# Date: 24-10-2012
# ---------------------------------------------------------------

import os
import sys

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

from django.core.paginator import Paginator

from django.utils import simplejson
from django.core import serializers
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.contrib.sites.models import get_current_site
import urlparse

# General Module imports-----------------------------------
from datetime import datetime, date, time


# Application Specific Model Imports-----------------------
from patient.models import *
from admission.models import *
#from discharge.models import *
#from visit.models     import *

import AuShadha.settings as settings

# Views start here -----------------------------------------

from patient.views import *

#


@login_required
def patient_medication_list_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                patient_medication_list_obj = PatientMedicationList(
                    patient_detail=patient_detail_obj)
                patient_medication_list_add_form = PatientMedicationListForm(
                    instance=patient_medication_list_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "patient_medication_list_add_form": patient_medication_list_add_form,
                                           "patient_medication_list_obj": patient_medication_list_obj,
                                           })
#      except TypeError or ValueError or AttributeError:
#        raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('patient/medication_list/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                patient_medication_list_obj = PatientMedicationList(
                    patient_detail=patient_detail_obj)
                patient_medication_list_add_form = PatientMedicationListForm(
                    request.POST, instance=patient_medication_list_obj)
                if patient_medication_list_add_form.is_valid():
                    medication_list_obj = patient_medication_list_add_form.save(
                    )
                    success = True
                    error_message = "MedicationList Data Added Successfully"
                    addData = {
                        "id": medication_list_obj.id,
                        "medication": medication_list_obj.medication,
                        "strength": medication_list_obj.strength,
                        "dosage": medication_list_obj.dosage,
                        "prescription_date": medication_list_obj.prescription_date.isoformat(),
                        "prescribed_by": medication_list_obj.prescribed_by,
                        "currently_active": medication_list_obj.currently_active,
                        "edit": medication_list_obj.get_edit_url(),
                        "del": medication_list_obj.get_del_url()
                    }
                    data = {'success': success,
                            'error_message': error_message,
                            "form_errors": None,
                            "addData": addData
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error Occured. MedicationList data could not be added."
                    form_errors = ''
                    for error in patient_medication_list_add_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404(
                "BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
    else:
        raise Http404("You need to Login")


@login_required
def patient_medication_list_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_medication_list_obj = PatientMedicationList.objects.get(
                    pk=id)
                patient_medication_list_edit_form = PatientMedicationListForm(
                    instance=patient_medication_list_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_medication_list_obj.patient_detail,
                                           "patient_medication_list_edit_form": patient_medication_list_edit_form,
                                           "patient_medication_list_obj": patient_medication_list_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientMedicationList.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('patient/medication_list/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_medication_list_obj = PatientMedicationList.objects.get(
                    pk=id)
                patient_medication_list_edit_form = PatientMedicationListForm(
                    request.POST, instance=patient_medication_list_obj)
                if patient_medication_list_edit_form.is_valid():
                    medication_list_obj = patient_medication_list_edit_form.save(
                    )
                    success = True
                    error_message = "MedicationList Data Edited Successfully"
                    addData = {
                        "id": medication_list_obj.id,
                        "medication": medication_list_obj.medication,
                        "strength": medication_list_obj.strength,
                        "dosage": medication_list_obj.dosage,
                        "prescription_date": medication_list_obj.prescription_date.isoformat(),
                        "prescribed_by": medication_list_obj.prescribed_by,
                        "currently_active": medication_list_obj.currently_active,
                        "edit": medication_list_obj.get_edit_url(),
                        "del": medication_list_obj.get_del_url()
                    }
                    data = {
                        'success': success,
                        'error_message': error_message,
                        "form_errors": None,
                        "addData": addData
                    }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error Occured. MedicationList data could not be added."
                    form_errors = ''
                    for error in patient_medication_list_edit_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404(
                "BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
    else:
        raise Http404("You need to Login")


@login_required
def patient_medication_list_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                patient_medication_list_obj = PatientMedicationList.objects.get(
                    pk=id)
                patient_detail_obj = patient_medication_list_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientMedicationList.DoesNotExist:
                raise Http404(
                    "BadRequest: Patient medication_list Data Does Not Exist")
            patient_medication_list_obj.delete()
            success = True
            error_message = "medication_list Data Deleted Successfully"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")
