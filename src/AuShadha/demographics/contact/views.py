################################################################################
# Project      : AuShadha
# Description  : Views for Contact
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
from .models import Contact, ContactForm



# Views start here -----------------------------------------

@login_required
def contact_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int(request.GET.get('patient_id'))
      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      contact_obj = Contact.objects.filter(patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(contact_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")

    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def contact_add(request, patient_id = None):

    if request.user:
        user = request.user

        try:
          if patient_id:
            patient_id = int(patient_id)
          else:
            patient_id = int(request.GET.get('patient_id'))

          patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
          patient_detail_obj.save()
          contact_obj = Contact(patient_detail=patient_detail_obj)

          if not getattr(patient_detail_obj, 'urls', None):
            patient_detail_obj.save()

          if request.method == "GET" and request.is_ajax():
              contact_form = ContactForm(instance=contact_obj, auto_id = False)
              variable = RequestContext(request,
                                        {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "contact_form": contact_form,
                                        "contact_obj": contact_obj,
                                        })
              return render_to_response('contact/add.html', variable)

          elif request.method == 'POST' and request.is_ajax():
              contact_form = ContactForm(request.POST, instance=contact_obj)
              if contact_form.is_valid():
                  contact_object = contact_form.save()
                  if not getattr(contact_object,'urls'):
                    contact_object.generate_urls()
                  success = True
                  error_message = "Contact Saved Successfully"
                  form_errors = None
                  addData = {
                      "id": contact_object.id,
                      'pat_id': contact_object.patient_detail.id,
                      "address_type": contact_object.address_type,
                      "address": contact_object.address,
                      "city": contact_object.city,
                      "state": contact_object.state,
                      "country": contact_object.country,
                      "pincode": contact_object.pincode,
                      "edit": contact_object.urls['edit'],
                      "del": contact_object.urls['del'],
                  }
              else:
                  success = False
                  error_message = aumodelformerrorformatter_factory(contact_form)
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
def contact_edit(request, contact_id = None):
    print "Received request for editing Contact"
    if request.user:
        user = request.user
        try:
          if contact_id: 
            contact_id = int(contact_id)
          else:
            contact_id = int(request.GET.get('contact_id'))

          contact_obj = Contact.objects.get(pk=contact_id)
          patient_detail_obj = contact_obj.patient_detail

          if not getattr(contact_obj,'urls'):
            contact_obj.generate_urls()

          if request.method == "GET" and request.is_ajax():

              contact_form = ContactForm(instance=contact_obj, auto_id = False)
              variable = RequestContext(request,
                                        {"user": user,
                                          "patient_detail_obj": patient_detail_obj,
                                          "contact_form": contact_form,
                                          "contact_obj": contact_obj,
                                          })
              return render_to_response('contact/edit.html', variable)

          elif request.method == 'POST' and request.is_ajax():
                  contact_form = ContactForm(request.POST, instance=contact_obj)
                  if contact_form.is_valid():
                      #print "now there are " , len(Contact.objects.all()), " Contact objects"
                      contact_object = contact_form.save()
                      #print "now there are " , len(Contact.objects.all()), " Contact objects"                      
                      success = True
                      error_message = "Contact Saved Successfully"
                      form_errors = None
                      data = {"success": success,
                              "error_message": error_message,
                              "form_errors": form_errors,
                              "id": contact_object.id,
                              'pat_id': contact_object.patient_detail.id,
                              "address_type": contact_object.address_type,
                              "address": contact_object.address,
                              "city": contact_object.city,
                              "state": contact_object.state,
                              "country": contact_object.country,
                              "pincode": contact_object.pincode,
                              "edit": contact_object.urls['edit'],
                              "del": contact_object.urls['del']
                              }
                  else:
                      success = False
                      error_message = aumodelformerrorformatter_factory(contact_form)
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

        except Contact.DoesNotExist:
            raise Http404("BadRequest: Contact Data Does Not Exist")


@login_required
def contact_del(request, contact_id  = None):
    user = request.user
    if request.user and user.is_superuser:

        if request.method == "GET":
            try:
                if contact_id:
                  contact_id = int(contact_id)
                else:
                  contact_id  = int(request.GET.get('contact_id') )
                contact_obj = Contact.objects.get(pk=contact_id)
                patient_detail_obj = contact_obj.patient_detail
                contact_obj.delete()
                success = True
                error_message = "Contact Data Deleted Successfully"
                data = {'success': success, 'error_message': error_message}
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')

            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Contact.DoesNotExist:
                raise Http404("BadRequest: Contact Data Does Not Exist")

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")