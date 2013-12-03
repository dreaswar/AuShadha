################################################################################
# Project      : AuShadha
# Description  : Views for Phone
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
from .models import Phone, PhoneForm



# Views start here -----------------------------------------

@login_required
def phone_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int(request.GET.get('patient_id'))
      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      phone_obj = Phone.objects.filter(patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(phone_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")

    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def phone_add(request, patient_id = None):

    if request.user:
        user = request.user

        try:
          if patient_id:
            patient_id = int(patient_id)
          else:
            patient_id = int(request.GET.get('patient_id'))

          patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
          phone_obj = Phone(patient_detail=patient_detail_obj)

          if not getattr(patient_detail_obj,'urls',None):
            patient_detail_obj.save()

          if request.method == "GET" and request.is_ajax():
              phone_form = PhoneForm(instance=phone_obj, auto_id = False )
              variable = RequestContext(request,
                                        {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "phone_form": phone_form,
                                        "phone_obj": phone_obj,
                                        })
              return render_to_response('phone/add.html', variable)

          elif request.method == 'POST' and request.is_ajax():
                  phone_form = PhoneForm(request.POST, instance=phone_obj)
                  if phone_form.is_valid():
                      phone_object = phone_form.save()

                      if not getattr(phone_object,'urls',None):
                        phone_object.generate_urls()                  

                      success = True
                      error_message = "Phone Saved Successfully"
                      form_errors = None
                      addData = {
                          "id": phone_object.id,
                          'pat_id': phone_object.patient_detail.id,
                          'phone_type': phone_object.phone_type,
                          'STD_Code': phone_object.STD_Code,
                          'ISD_Code': phone_object.ISD_Code,
                          'phone': phone_object.phone,
                          "edit": phone_object.urls['edit'],
                          "del": phone_object.urls['del'],
                      }
                  else:
                      success = False
                      error_message = aumodelformerrorformatter_factory(phone_form)
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
def phone_edit(request, phone_id):
    if request.user:
        user = request.user
        try:
          if phone_id: 
            phone_id = int(phone_id)
          else:
            phone_id = int(request.GET.get('phone_id'))

          phone_obj = Phone.objects.get(pk=phone_id)
          patient_detail_obj = phone_obj.patient_detail

          if not getattr(phone_obj,'urls'):
            phone_obj.generate_urls()                  

          if request.method == "GET" and request.is_ajax():
              phone_form = PhoneForm(instance=phone_obj, auto_id = False )
              variable = RequestContext(request,
                                        {"user": user,
                                          "patient_detail_obj": patient_detail_obj,
                                          "phone_form": phone_form,
                                          "phone_obj": phone_obj,
                                          })
              return render_to_response('phone/edit.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              phone_form = PhoneForm(request.POST, instance=phone_obj)
              if phone_form.is_valid():
                  phone_object = phone_form.save()
                  success = True
                  error_message = "Phone Saved Successfully"
                  form_errors = None
                  data = {"success": success,
                          "error_message": error_message,
                          "form_errors": form_errors,
                          "id": phone_object.id,
                          'phone_type': phone_object.phone_type,
                          'STD_Code': phone_object.STD_Code,
                          'ISD_Code': phone_object.ISD_Code,
                          'phone': phone_object.phone,
                          'pat_id': phone_object.patient_detail.id,
                          "edit": phone_object.urls['edit'],
                          "del": phone_object.urls['del']
                          }
              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(phone_form)
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

        except Phone.DoesNotExist:
            raise Http404("BadRequest: Phone Data Does Not Exist")


@login_required
def phone_del(request, phone_id  = None):
    user = request.user
    if request.user and user.is_superuser:

        if request.method == "GET":
            try:
                if phone_id:
                  phone_id = int(phone_id)
                else:
                  phone_id  = int(request.GET.get('phone_id') )
                phone_obj = Phone.objects.get(pk=phone_id)
                patient_detail_obj = phone_obj.patient_detail
                phone_obj.delete()
                success = True
                error_message = "Phone Data Deleted Successfully"
                data = {'success': success, 'error_message': error_message}
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')

            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Phone.DoesNotExist:
                raise Http404("BadRequest: Phone Data Does Not Exist")

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")