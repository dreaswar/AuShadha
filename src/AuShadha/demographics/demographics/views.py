################################################################################
# Project      : AuShadha
# Description  : Views for Demographics
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
from .models import Demographics, DemographicsForm



# Views start here -----------------------------------------

@login_required
def demographics_json(request, patient_id = None):

    try:
        if patient_id:
          patient_id = int(patient_id)
        else:
          patient_id = int(request.GET.get('patient_id'))
          action = unicode(request.GET.get('action'))        
          if action == 'add':
              return demographics_add(request, patient_id)

        patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
        demographics_obj = Demographics.objects.filter(patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(demographics_obj)
        return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
      raise Http404("ERROR:: Bad request.Invalid arguments passed")

    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def demographics_add(request, patient_id = None):
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
          demographics_obj = Demographics.objects.filter(patient_detail=patient_detail_obj)

          if not demographics_obj:
              demographics_obj = Demographics(patient_detail=patient_detail_obj)            
          else:
              demographics_obj = demographics_obj[0]
              return demographics_edit(request, demographics_id = demographics_obj.id)

          if request.method == "GET" and request.is_ajax():
                demographics_form = DemographicsForm(instance=demographics_obj, auto_id = False)
                variable = RequestContext(request,
                                          {"user": user,
                                            "patient_detail_obj": patient_detail_obj,
                                            "demographics_form": demographics_form,
                                            "demographics_obj": demographics_obj,
                                            'button_label': "Add",
                                            "action": p_urls['add']['demographics'],
                                            "addUrl": p_urls['add']['demographics'],
                                            'canDel': False,
                                            'editUrl': None,
                                            'delUrl': None
                                          })
                return render_to_response('demographics/add_or_edit_form.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              demographics_form = DemographicsForm(request.POST, instance=demographics_obj)

              if demographics_form.is_valid():

                  try:
                    demographics_obj = demographics_form.save()
                    success = True
                    error_message = "Demographics Data Added Successfully"
                    form_errors = None
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors,
                            'canDel': True,
                            'addUrl': None,
                            'editUrl': demographics_obj.urls['edit'],
                            'delUrl': demographics_obj.urls['del'],
                            }

                  except (DemographicsDataExistsError):
                    success = False
                    error_message = "Demographics Data Already Exists ! Cannot add more.."
                    form_errors = ''
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors
                            }

              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(demographics_form)
                  form_errors = error_message
                  data = {'success': success,
                          'error_message': error_message,
                          'form_errors': form_errors
                          }
              json = simplejson.dumps(data)
              return HttpResponse(json, content_type='application/json')

          else:
              raise Http404("BadRequest: Unsupported Request Method")

        except ValueError or AttributeError or TypeError:
            raise Http404("BadRequest: Server Error")

        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Requested Patient DoesNotExist")



@login_required
def demographics_edit(request, demographics_id  = None):
    if request.user:
        user = request.user
        try:
          if demographics_id:
            demographics_id = int(demographics_id)
          else:
            demographics_id = int(request.GET.get('demographics_id'))

          demographics_obj = Demographics.objects.get(pk=demographics_id)
          patient_detail_obj = demographics_obj.patient_detail
          demographics_obj.save()
          d_urls = demographics_obj.urls

        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")

        except Demographics.DoesNotExist:
            raise Http404("BadRequest: Patient DemographicsData Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            demographics_form = DemographicsForm(instance=demographics_obj, auto_id = False )
            variable = RequestContext(request,
                                      {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "demographics_form": demographics_form,
                                        "demographics_obj": demographics_obj,
                                        'action': d_urls['edit'],
                                        'button_label': "Edit",
                                        'canDel': True,
                                        'addUrl': None,
                                        'editUrl': d_urls['edit'],
                                        'delUrl': d_urls['del'],
                                        })
            return render_to_response('demographics/add_or_edit_form.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            demographics_form = DemographicsForm(request.POST, instance=demographics_obj)

            if demographics_form.is_valid():
                demographics_obj = demographics_form.save()
                success = True
                error_message = "Demographics Data Edited Successfully"
                form_errors = None

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(demographics_form)
                form_errors = error_message

            data = {'success': success, 
                    'error_message': error_message, 
                    'form_errors':form_errors
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
    
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def demographics_del(request, demographics_id = None):
    user = request.user
    if user and user.is_superuser:
        try:
          if demographics_id:
            demographics_id = int(demographics_id)
          else:
            demographics_id = int(request.GET.get('demographics_id'))

          demographics_obj = Demographics.objects.get(pk=demographics_id)
          patient_detail_obj = demographics_obj.patient_detail
          patient_detail_obj.save()
          p_urls = patient_detail_obj.urls

          if request.method == "GET":
            demographics_obj.delete()
            success = True
            error_message = "Demographics Data Deleted Successfully"
            data = {'success': success,
                    'error_message': error_message,
                    'addUrl': p_urls['add']['demographics'],
                    'canDel': False,
                    'editUrl': None,
                    'delUrl': None
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

          else:
              raise Http404("BadRequest: Unsupported Request Method")

        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")

        except Demographics.DoesNotExist:
            raise Http404("BadRequest: Patient DemographicsData Data Does Not Exist")

    else:
        raise Http404("Server Error: No Permission to delete.")