################################################################################
# Project      : AuShadha
# Description  : Views for Immunisation display and modification.
# Author       : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date         : 16-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

#from django.core.context_processors import csrf
#from django.contrib.auth.models import User
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder


#Utilities
from core.serializers.data_grid import generate_json_for_datagrid

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from patient.models import PatientDetail
from immunisation.models import Immunisation, ImmunisationForm



# Views start here -----------------------------------------

@login_required
def immunisation_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return immunisation_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
        immunisation_obj = Immunisation.objects.filter(
            patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(immunisation_obj)
        return HttpResponse(json, content_type="application/json")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")

@login_required
def immunisation_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                immunisation_obj = Immunisation(
                    patient_detail=patient_detail_obj)
                immunisation_add_form = ImmunisationForm(
                    instance=immunisation_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "immunisation_add_form": immunisation_add_form,
                                           "immunisation_obj": immunisation_obj,
                                           })
            except TypeError or ValueError or AttributeError:
              raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('immunisation/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                immunisation_obj = Immunisation(
                    patient_detail=patient_detail_obj, administrator=user)
                immunisation_add_form = ImmunisationForm(
                    request.POST, instance=immunisation_obj)
                if immunisation_add_form.is_valid():
                    immunisation_obj = immunisation_add_form.save(
                    )
                    success = True
                    error_message = "Immunisation Data Added Successfully"
                    addData = {
                        "id": immunisation_obj.id,
                        "vaccine_detail": immunisation_obj.vaccine_detail.vaccine_name,
                        "vaccination_date": immunisation_obj.vaccination_date.isoformat(),
                        "next_due": immunisation_obj.next_due.isoformat(),
                        "route": immunisation_obj.route,
                        "injection_site": immunisation_obj.injection_site,
                        "dose": immunisation_obj.dose,
                        "administrator": immunisation_obj.administrator.__unicode__(),
                        "adverse_reaction": immunisation_obj.adverse_reaction,
                        "edit": immunisation_obj.get_edit_url(),
                        "del": immunisation_obj.get_del_url()
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
                    error_message = "Error Occured. Immunisation data could not be added."
                    form_errors = ''
                    for error in immunisation_add_form.errors:
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
def immunisation_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                immunisation_obj = Immunisation.objects.get(
                    pk=id)
                immunisation_edit_form = ImmunisationForm(
                    instance=immunisation_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": immunisation_obj.patient_detail,
                                           "immunisation_edit_form": immunisation_edit_form,
                                           "immunisation_obj": immunisation_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Immunisation.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('immunisation/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                immunisation_obj = Immunisation.objects.get(
                    pk=id)
                immunisation_edit_form = ImmunisationForm(
                    request.POST, instance=immunisation_obj)
                if immunisation_edit_form.is_valid():
                    immunisation_obj = immunisation_edit_form.save(
                    )
                    success = True
                    error_message = "Immunisation Data Edited Successfully"
                    addData = {
                        "id": immunisation_obj.id,
                        "vaccine_detail": immunisation_obj.vaccine_detail.vaccine_name,
                        "vaccination_date": immunisation_obj.vaccination_date.isoformat(),
                        "next_due": immunisation_obj.next_due.isoformat(),
                        "route": immunisation_obj.route,
                        "injection_site": immunisation_obj.injection_site,
                        "dose": immunisation_obj.dose,
                        "administrator": immunisation_obj.administrator.__unicode__(),
                        "adverse_reaction": immunisation_obj.adverse_reaction,
                        "edit": immunisation_obj.get_edit_url(),
                        "del": immunisation_obj.get_del_url()
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
                    error_message = "Error Occured. Immunisation data could not be added."
                    form_errors = ''
                    for error in immunisation_edit_form.errors:
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
def immunisation_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                immunisation_obj = Immunisation.objects.get(
                    pk=id)
                patient_detail_obj = immunisation_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Immunisation.DoesNotExist:
                raise Http404(
                    "BadRequest: Immunisation Data Does Not Exist")
            immunisation_obj.delete()
            success = True
            error_message = "immunisation Data Deleted Successfully"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")
