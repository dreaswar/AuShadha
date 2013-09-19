###############################################################################
# Project     : AuShadha
# Description : Views for Patient Allergy recording, editing and deleting
# Author      : Dr.Easwar T.R 
# Date        : 16-09-2013
###############################################################################


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
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from core.serializers.data_grid import generate_json_for_datagrid
from patient.models import PatientDetail
from allergy_list.models import Allergy, AllergyForm


# Views start here -----------------------------------------

@login_required
def allergy_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return allergy_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
        allergy_obj = Allergy.objects.filter(
            patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(allergy_obj)
        return HttpResponse(json, content_type="application/json")
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
      raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")



@login_required
def allergy_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                allergy_obj = Allergy(
                    patient_detail=patient_detail_obj)
                allergy_add_form = AllergyForm(
                    instance=allergy_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "allergy_add_form": allergy_add_form,
                                           "allergy_obj": allergy_obj,
                                           })
            except TypeError or ValueError or AttributeError:
              raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('allergy/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                allergy_obj = Allergy(
                    patient_detail=patient_detail_obj)
                allergy_add_form = AllergyForm(
                    request.POST, instance=allergy_obj)
                if allergy_add_form.is_valid():
                    allergy_obj = allergy_add_form.save()
                    success = True
                    error_message = "Allergy Data Added Successfully"
                    addData = {
                        "id": allergy_obj.id,
                        "allergic_to": allergy_obj.allergic_to,
                        "reaction_observed": allergy_obj.reaction_observed,
                        "edit": allergy_obj.get_edit_url(),
                        "del": allergy_obj.get_del_url()
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
                    error_message = "Error Occured. Allergy data could not be added."
                    form_errors = ''
                    for error in allergy_add_form.errors:
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
def allergy_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                allergy_obj = Allergy.objects.get(
                    pk=id)
                allergy_edit_form = AllergyForm(
                    instance=allergy_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": allergy_obj.patient_detail,
                                           "allergy_edit_form": allergy_edit_form,
                                           "allergy_obj": allergy_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Allergy.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('allergy/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                allergy_obj = Allergy.objects.get(
                    pk=id)
                allergy_edit_form = AllergyForm(
                    request.POST, instance=allergy_obj)
                if allergy_edit_form.is_valid():
                    allergy_obj = allergy_edit_form.save(
                    )
                    success = True
                    error_message = "Allergy Data Edited Successfully"
                    addData = {
                        "id": allergy_obj.id,
                        "allergic_to": allergy_obj.allergic_to,
                        "reaction_observed": allergy_obj.reaction_observed,
                        "edit": allergy_obj.get_edit_url(),
                        "del": allergy_obj.get_del_url()
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
                    error_message = "Error Occured. Allergy data could not be added."
                    form_errors = ''
                    for error in allergy_edit_form.errors:
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
def allergy_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                allergy_obj = Allergy.objects.get(pk=id)
                patient_detail_obj = allergy_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Allergy.DoesNotExist:
                raise Http404(
                    "BadRequest: Allergy Data Does Not Exist")
            allergy_obj.delete()
            success = True
            error_message = "allergy Data Deleted Successfully"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")

