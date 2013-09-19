################################################################################
# Project      : AuShadha
# Description  : Medical History Views
# Author       : Dr.Easwar T.R 
# Date         : 16-09-2013
# License      : GNU-GPL Version 3,Please see AuShadha/LICENSE.txt for details
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models import User


#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core.paginator import Paginator
#from django.template.response import TemplateResponse
#from django.contrib.sites.models import get_current_site
#import urlparse
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from core.serializers.data_grid import generate_json_for_datagrid

from patient.models import PatientDetail



# Views start here -----------------------------------------
@login_required
def medical_history_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return medical_history_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
        medical_history_obj = MedicalHistory.objects.filter(
            patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(medical_history_obj)
        return HttpResponse(json, content_type="application/json")
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def medical_history_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                medical_history_obj = MedicalHistory(
                    patient_detail=patient_detail_obj)
                medical_history_add_form = MedicalHistoryForm(
                    instance=medical_history_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "medical_history_add_form": medical_history_add_form,
                                           "medical_history_obj": medical_history_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('medical_history/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                medical_history_obj = MedicalHistory(
                    patient_detail=patient_detail_obj)
                medical_history_add_form = MedicalHistoryForm(
                    request.POST, instance=medical_history_obj)
                if medical_history_add_form.is_valid():
                    medical_history_obj = medical_history_add_form.save(
                    )
                    success = True
                    error_message = "Medical History Data Added Successfully"
                    addData = {
                        "id": medical_history_obj.id,
                        "disease": medical_history_obj.disease,
                        "icd_10_code": getattr(medical_history_obj, 'icd_10_code.__unicode__()', None),
                        "status": medical_history_obj.status,
                        "active": medical_history_obj.active,
                        "infectious_disease": medical_history_obj.infectious_disease,
                        "severity": medical_history_obj.severity,
                        "allergic_disease": medical_history_obj.allergic_disease,
                        "pregnancy_warning": medical_history_obj.pregnancy_warning,
                        "date_of_diagnosis": getattr(medical_history_obj, 'date_of_diagnosis.isoformat()', None),
                        "healed": medical_history_obj.healed,
                        "remarks": medical_history_obj.remarks,
                        "edit": medical_history_obj.get_edit_url(),
                        "del": medical_history_obj.get_del_url()
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
                    error_message = "Error Occured. Medical History data could not be added."
                    form_errors = ''
                    for error in medical_history_add_form.errors:
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
def medical_history_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                medical_history_obj = MedicalHistory.objects.get(
                    pk=id)
                medical_history_edit_form = MedicalHistoryForm(
                    instance=medical_history_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": medical_history_obj.patient_detail,
                                           "medical_history_edit_form": medical_history_edit_form,
                                           "medical_history_obj": medical_history_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except MedicalHistory.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('medical_history/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                medical_history_obj = MedicalHistory.objects.get(
                    pk=id)
                medical_history_edit_form = MedicalHistoryForm(
                    request.POST, instance=medical_history_obj)
                if medical_history_edit_form.is_valid():
                    medical_history_obj = medical_history_edit_form.save(
                    )
                    success = True
                    error_message = "Medical History Data Edited Successfully"
                    addData = {
                        "id": medical_history_obj.id,
                        "disease": medical_history_obj.disease,
                        "icd_10_code": getattr(medical_history_obj, 'icd_10_code.__unicode__()', None),
                        "status": medical_history_obj.status,
                        "active": medical_history_obj.active,
                        "infectious_disease": medical_history_obj.infectious_disease,
                        "severity": medical_history_obj.severity,
                        "allergic_disease": medical_history_obj.allergic_disease,
                        "pregnancy_warning": medical_history_obj.pregnancy_warning,
                        "date_of_diagnosis": getattr(medical_history_obj, 'date_of_diagnosis.isoformat()', None),
                        "healed": medical_history_obj.healed,
                        "remarks": medical_history_obj.remarks,
                        "edit": medical_history_obj.get_edit_url(),
                        "del": medical_history_obj.get_del_url()
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
                    error_message = "Error Occured. Medical History data could not be added."
                    form_errors = ''
                    for error in medical_history_edit_form.errors:
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
def medical_history_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                medical_history_obj = MedicalHistory.objects.get(
                    pk=id)
                patient_detail_obj = medical_history_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except MedicalHistory.DoesNotExist:
                raise Http404(
                    "BadRequest: Medical History Data Does Not Exist")
            medical_history_obj.delete()
            success = True
            error_message = "Medical History Data Deleted Successfully"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")
