################################################################################
# Project      : AuShadha
# Description  : Views for Guardian
# Author       : Dr.Easwar T.R 
# Date         : 04-10-2013
# License      : GNU-GPL Version 3, See LICENSE.txt 
################################################################################

import os
import sys
from datetime import datetime, date, time

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory

#from patient.models import PatientDetail
PatientDetail = UI.get_module("PatientRegistration")
from .models import Guardian, GuardianForm



# Views start here -----------------------------------------

@login_required
def guardian_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int(request.GET.get('patient_id'))
      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      guardian_obj = Guardian.objects.filter(patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(guardian_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")

    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def guardian_add(request, patient_id = None):

    if request.user:
        user = request.user

        try:
          if patient_id:
            patient_id = int(patient_id)
          else:
            patient_id = int(request.GET.get('patient_id'))

          patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
          patient_detail_obj.save()
          p_urls = patient_detail_obj.urls
          guardian_obj = Guardian(patient_detail=patient_detail_obj)

          if request.method == "GET" and request.is_ajax():
              guardian_form = GuardianForm(instance=guardian_obj, auto_id = False )
              variable = RequestContext(request,
                                        {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "guardian_form": guardian_form,
                                        "guardian_obj": guardian_obj,
                                        'addUrl': p_urls['add']['guardian']
                                        })
              return render_to_response('guardian/add.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              guardian_form = GuardianForm(request.POST, instance=guardian_obj)
              if guardian_form.is_valid():
                  guardian_object = guardian_form.save()
                  if not getattr(guardian_object,'urls'):
                    guardian_object.generate_urls()                                    
                  success = True
                  error_message = "Guardian Saved Successfully"
                  form_errors = None
                  addData = {
                      "id": guardian_object.id,
                      'pat_id': guardian_object.patient_detail.id,
                      "guardian_name": guardian_object.guardian_name,
                      "relation_to_guardian": guardian_object.relation_to_guardian,
                      "guardian_phone": guardian_object.guardian_phone,       
                      "edit": guardian_object.urls['edit'],
                      "del": guardian_object.urls['del'],
                  }
              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(guardian_form)
                  form_errors = error_message
                  addData = None
              data = {"success": success,
                      "error_message": error_message,
                      "form_errors": form_errors,
                      "addData": addData
                      }
              json = simplejson.dumps(data)
              return HttpResponse(json, content_type='application/json')

          else:
              raise Http404("BadRequest: Unsupported Request Method")

        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")
        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")          



@login_required
def guardian_edit(request, guardian_id):
    if request.user:
        user = request.user
        try:
          if guardian_id: 
            guardian_id = int(guardian_id)
          else:
            guardian_id = int(request.GET.get('guardian_id'))

          guardian_obj = Guardian.objects.get(pk=guardian_id)
          patient_detail_obj = guardian_obj.patient_detail

          if not getattr(guardian_obj,'urls'):
              guardian_obj.generate_urls()                  

          if request.method == "GET" and request.is_ajax():
              guardian_form = GuardianForm(instance=guardian_obj, auto_id = False )
              variable = RequestContext(request,
                                        {"user": user,
                                          "patient_detail_obj": patient_detail_obj,
                                          "guardian_form": guardian_form,
                                          "guardian_obj": guardian_obj,
                                          })
              return render_to_response('guardian/edit.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              guardian_form = GuardianForm(request.POST, instance=guardian_obj)

              if guardian_form.is_valid():
                  guardian_object = guardian_form.save()
                  success = True
                  error_message = "Guardian Saved Successfully"
                  form_errors = None
                  data = {"success": success,
                          "error_message": error_message,
                          "form_errors": form_errors,
                          "id": guardian_object.id,
                          'pat_id': guardian_object.patient_detail.id,
                          "guardian_name": guardian_object.guardian_name,
                          "relation_to_guardian": guardian_object.relation_to_guardian,
                          "guardian_phone": guardian_object.guardian_phone,       
                          "edit": guardian_object.urls['edit'],
                          "del": guardian_object.urls['del']
                  }

              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(guardian_form)
                  form_errors = error_message
                  data = {'success'       : success,
                          'error_message' : error_message,
                          'form_errors'   : form_errors
                          }
              json = simplejson.dumps(data)
              return HttpResponse(json, content_type='application/json')

          else:
              raise Http404("BadRequest: Unsupported Request Method")

        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")

        except Guardian.DoesNotExist:
            raise Http404("BadRequest: Guardian Data Does Not Exist")


@login_required
def guardian_del(request, guardian_id  = None):
    user = request.user
    if request.user and user.is_superuser:

        if request.method == "GET":
            try:
                if guardian_id:
                  guardian_id = int(guardian_id)
                else:
                  guardian_id  = int(request.GET.get('guardian_id') )
                guardian_obj = Guardian.objects.get(pk=guardian_id)
                patient_detail_obj = guardian_obj.patient_detail
                guardian_obj.delete()
                success = True
                error_message = "Guardian Data Deleted Successfully"
                data = {'success': success, 'error_message': error_message}
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')

            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Guardian.DoesNotExist:
                raise Http404("BadRequest: Guardian Data Does Not Exist")

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")