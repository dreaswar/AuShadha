################################################################################
# PROJECT      : AuShadha
# Description  : SurgicalHistory views
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core.paginator import Paginator
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder
#from django.template.response import TemplateResponse
#from django.contrib.sites.models import get_current_site
#import urlparse


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL

from patient.models import PatientDetail
from surgical_history.models import SurgicalHistory,SurgicalHistoryForm


# Views start here -----------------------------------------
@login_required
def surgical_history_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return surgical_history_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
        surgical_history_obj = SurgicalHistory.objects.filter(
            patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(surgical_history_obj)
        return HttpResponse(json, content_type="application/json")
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def surgical_history_add(request, id):
    if request.user:
        user = request.user
        print "Request received for adding Surgical History"
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                surgical_history_obj = SurgicalHistory(
                    patient_detail=patient_detail_obj)
                surgical_history_form = SurgicalHistoryForm(
                    instance=surgical_history_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "surgical_history_form": surgical_history_form,
                                           "surgical_history_obj": surgical_history_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('surgical_history/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                surgical_history_obj = SurgicalHistory(
                    patient_detail=patient_detail_obj)
                surgical_history_form = SurgicalHistoryForm(
                    request.POST, instance=surgical_history_obj)
                if surgical_history_form.is_valid():
                    surgical_history_obj = surgical_history_form.save(
                    )
                    success = True
                    error_message = "Surgical History Data Added Successfully"
                    addData = {
                        "id": surgical_history_obj.id,
                        "description": surgical_history_obj.description,
                        "icd_10_code": getattr(surgical_history_obj, 'icd_10_code.__unicode__()', None),
                        "cpc_code": getattr(surgical_history_obj, 'cpc_code.__unicode__()', None),
                        "base_condition": surgical_history_obj.base_condition,
                        "med_condition": getattr(surgical_history_obj, 'med_condition.__unicode__()', None),
                        "classification": surgical_history_obj.classification,
                        "healed": surgical_history_obj.healed,
                        "date_of_surgery": getattr(surgical_history_obj, 'date_of_surgery.isoformat()', None),
                        "remarks": surgical_history_obj.remarks,
                        "edit": surgical_history_obj.get_edit_url(),
                        "del": surgical_history_obj.get_del_url()
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
                    error_message = "Error Occured. Surgical History data could not be added."
                    form_errors = ''
                    for error in surgical_history_form.errors:
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
def surgical_history_edit(request, id):
    if request.user:
        user = request.user
        print "Request received for editing Surgical History"
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                surgical_history_obj = SurgicalHistory.objects.get(
                    pk=id)
                surgical_history_form = SurgicalHistoryForm(
                    instance=surgical_history_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": surgical_history_obj.patient_detail,
                                           "surgical_history_form": surgical_history_form,
                                           "surgical_history_obj": surgical_history_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except SurgicalHistory.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('surgical_history/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                surgical_history_obj = SurgicalHistory.objects.get(
                    pk=id)
                surgical_history_form = SurgicalHistoryForm(
                    request.POST, instance=surgical_history_obj)
                if surgical_history_form.is_valid():
                    surgical_history_obj = surgical_history_form.save(
                    )
                    success = True
                    error_message = "Surgical History Data Edited Successfully"
                    addData = {
                        "id": surgical_history_obj.id,
                        "description": surgical_history_obj.description,
                        "icd_10_code": getattr(surgical_history_obj, 'icd_10_code.__unicode__()', None),
                        "cpc_code": getattr(surgical_history_obj, 'cpc_code.__unicode__()', None),
                        "base_condition": surgical_history_obj.base_condition,
                        "med_condition": getattr(surgical_history_obj, 'med_condition.__unicode__()', None),
                        "classification": surgical_history_obj.classification,
                        "healed": surgical_history_obj.healed,
                        "date_of_surgery": getattr(surgical_history_obj, 'date_of_surgery.isoformat()', None),
                        "remarks": surgical_history_obj.remarks,
                        "edit": surgical_history_obj.get_edit_url(),
                        "del": surgical_history_obj.get_del_url()
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
                    error_message = "Error Occured. Surgical History data could not be added."
                    form_errors = ''
                    for error in surgical_history_form.errors:
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
def surgical_history_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                surgical_history_obj = SurgicalHistory.objects.get(
                    pk=id)
                patient_detail_obj = surgical_history_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except SurgicalHistory.DoesNotExist:
                raise Http404(
                    "BadRequest: Surgical History Data Does Not Exist")
            surgical_history_obj.delete()
            success = True
            error_message = "Surgical History Data Deleted Successfully"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")

