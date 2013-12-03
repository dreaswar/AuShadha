################################################################################
# Project      : AuShadha
# Description  : Views for EmailAndFax
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
from .models import EmailAndFax, EmailAndFaxForm



# Views start here -----------------------------------------

@login_required
def email_and_fax_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int(request.GET.get('patient_id'))
      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      email_and_fax_obj = EmailAndFax.objects.filter(patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(email_and_fax_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")

    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def email_and_fax_add(request, patient_id = None):

    if request.user:
        user = request.user

        try:
          if patient_id:
            patient_id = int(patient_id)
          else:
            patient_id = int(request.GET.get('patient_id'))

          patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
          email_and_fax_obj = EmailAndFax(patient_detail=patient_detail_obj)

          if request.method == "GET" and request.is_ajax():
              email_and_fax_form = EmailAndFaxForm(instance=email_and_fax_obj, auto_id = False )
              variable = RequestContext(request,
                                        {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "email_and_fax_form": email_and_fax_form,
                                        "email_and_fax_obj": email_and_fax_obj,
                                        })
              return render_to_response('email_and_fax/add.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              email_and_fax_form = EmailAndFaxForm(request.POST, instance=email_and_fax_obj)
              if email_and_fax_form.is_valid():
                  email_and_fax_object = email_and_fax_form.save()
                  if not getattr(email_and_fax_object,'urls'):
                    email_and_fax_object.generate_urls()                                    
                  success = True
                  error_message = "EmailAndFax Saved Successfully"
                  form_errors = None
                  addData = {
                            "id": email_and_fax_object.id,
                            'pat_id': email_and_fax_object.patient_detail.id,
                            "email": email_and_fax_object.email,
                            "fax": email_and_fax_object.fax,
                            "web": email_and_fax_object.web,
                            "edit": email_and_fax_object.urls['edit'],
                            "del": email_and_fax_object.urls['del'],
                  }
              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(email_and_fax_form)
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
def email_and_fax_edit(request, email_and_fax_id):
    if request.user:
        user = request.user
        try:
          if email_and_fax_id: 
            email_and_fax_id = int(email_and_fax_id)
          else:
            email_and_fax_id = int(request.GET.get('email_and_fax_id'))

          email_and_fax_obj = EmailAndFax.objects.get(pk=email_and_fax_id)
          patient_detail_obj = email_and_fax_obj.patient_detail

          if not getattr(email_and_fax_obj,'urls'):
            email_and_fax_obj.generate_urls()

          if request.method == "GET" and request.is_ajax():
              email_and_fax_form = EmailAndFaxForm(instance=email_and_fax_obj, auto_id = False )
              variable = RequestContext(request,
                                        {"user": user,
                                          "patient_detail_obj": patient_detail_obj,
                                          "email_and_fax_form": email_and_fax_form,
                                          "email_and_fax_obj": email_and_fax_obj,
                                          })
              return render_to_response('email_and_fax/edit.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              email_and_fax_form = EmailAndFaxForm(request.POST, instance=email_and_fax_obj)
              if email_and_fax_form.is_valid():
                  email_and_fax_object = email_and_fax_form.save()
                  success = True
                  error_message = "EmailAndFax Saved Successfully"
                  form_errors = None
                  data = {"success": success,
                          "error_message": error_message,
                          "form_errors": form_errors,
                          "id": email_and_fax_object.id,
                          "email": email_and_fax_object.email,
                          "fax": email_and_fax_object.fax,
                          "web": email_and_fax_object.web,
                          'pat_id': email_and_fax_object.patient_detail.id,
                          "edit": email_and_fax_object.urls['edit'],
                          "del": email_and_fax_object.urls['del']
                          }
              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(email_and_fax_form)
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

        except EmailAndFax.DoesNotExist:
            raise Http404("BadRequest: EmailAndFax Data Does Not Exist")


@login_required
def email_and_fax_del(request, email_and_fax_id  = None):
    user = request.user
    if request.user and user.is_superuser:

        if request.method == "GET":
            try:
                if email_and_fax_id:
                  email_and_fax_id = int(email_and_fax_id)
                else:
                  email_and_fax_id  = int(request.GET.get('email_and_fax_id') )
                email_and_fax_obj = EmailAndFax.objects.get(pk=email_and_fax_id)
                patient_detail_obj = email_and_fax_obj.patient_detail
                email_and_fax_obj.delete()
                success = True
                error_message = "EmailAndFax Data Deleted Successfully"
                data = {'success': success, 'error_message': error_message}
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')

            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except EmailAndFax.DoesNotExist:
                raise Http404("BadRequest: EmailAndFax Data Does Not Exist")

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")