################################################################################
# Project      : AuShadha
# Description  : MedicationList Views
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

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory

from patient.models import PatientDetail
from medication_list.models import MedicationList, MedicationListForm


# Views start here -----------------------------------------
@login_required
def medication_list_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id  = int(patient_id)
      else:
        action = unicode(request.GET.get('action'))
        patient_id = int(request.GET.get('patient_id'))

        if action == 'add':
            return medication_list_add(request, patient_id)

      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      medication_list_obj = MedicationList.objects.filter(
          patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(medication_list_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def medication_list_add(request, patient_id = None):

    success = True
    error_message = None
    form_errors = None
    addData = None

    if request.user:
        user = request.user
        try:
          if patient_id:
            patient_id = int(patient_id)
          else:
            patient_id  = int(request.GET.get('patient_id'))
          patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
          patient_detail_obj.generate_urls()
          p_urls = patient_detail_obj.urls
          medication_list_obj = MedicationList(patient_detail=patient_detail_obj)
        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")
        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            medication_list_form = MedicationListForm( instance=medication_list_obj)
            variable = RequestContext(request,
                                      {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "medication_list_form": medication_list_form,
                                        "medication_list_obj": medication_list_obj,
                                        'addUrl' : p_urls['add']['medication_list']
                                        })
            return render_to_response('medication_list/add.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            medication_list_form = MedicationListForm(request.POST, 
                                                      instance=medication_list_obj)
            if medication_list_form.is_valid():
                medication_list_obj = medication_list_form.save()
                medication_list_obj.generate_urls()
                m_urls = medication_list_obj.urls
                print "MedicationList URLS: "
                print m_urls
                patient_detail_obj.generate_urls()
                p_urls = patient_detail_obj.urls

                fields_list = [field for field in medication_list_obj._meta.fields if field.serialize]

                success = True
                error_message = "MedicationList Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(medication_list_obj) for f in fields_list}
                addData['add'] = p_urls['add']['medication_list']
                addData['json']= p_urls['json']['medication_list']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(medication_list_form)
                form_errors = True
                addData = None

            data = {
                'success': success,
                'error_message': error_message,
                "form_errors": None,
                "addData": addData
            }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("You need to Login")



@login_required
def medication_list_edit(request, medication_list_id = None):

    if request.user:
        user = request.user
        try:
          medication_list_id = int(medication_list_id)
          medication_list_obj = MedicationList.objects.get(pk= medication_list_id)
          medication_list_obj.generate_urls()
          m_urls = medication_list_obj.urls

        except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
        except MedicationList.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            print "Received request for Editing MedicationList"
            print "MedicationList URLS is, ", m_urls
            medication_list_form = MedicationListForm(instance=medication_list_obj)
            variable = RequestContext(request,
                                      { "user": user,
                                        "patient_detail_obj"  : medication_list_obj.patient_detail,
                                        "medication_list_form": medication_list_form,
                                        "medication_list_obj" : medication_list_obj,
                                        'editUrl'            : m_urls['edit'],
                                        'delUrl'             : m_urls['del'],
                                      })
            return render_to_response('medication_list/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            medication_list_form = MedicationListForm(request.POST, 
                                                           instance=medication_list_obj)

            if medication_list_form.is_valid():
                medication_list_obj = medication_list_form.save()

                medication_list_obj.generate_urls()
                m_urls = medication_list_obj.urls

                medication_list_obj.patient_detail.generate_urls()
                p_urls = medication_list_obj.patient_detail.urls

                fields_list = [field for field in medication_list_obj._meta.fields if field.serialize]

                success = True
                error_message = "MedicationList Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(medication_list_obj) for f in fields_list}
                addData['add'] = p_urls['add']['medication_list']
                addData['json']= p_urls['json']['medication_list']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(medication_list_form)
                form_errors = True
                addData = None

            data = {
                'success': success,
                'error_message': error_message,
                "form_errors": None,
                "addData": addData
            }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("You need to Login")


@login_required
def medication_list_del(request, medication_list_id = None):
    user = request.user

    if request.user and user.is_superuser:

        if request.method == "GET":

            try:
                if medication_list_id: 
                  medication_list_id = int(medication_list_id)
                else:
                  medication_list_id = int(request.GET.get('medication_list_id'))
                medication_list_obj = MedicationList.objects.get(pk=medication_list_id)
                patient_detail_obj = medication_list_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except MedicationList.DoesNotExist:
                raise Http404(
                    "BadRequest: MedicationList Data Does Not Exist")

            medication_list_obj.delete()
            success = True
            error_message = "MedicationList Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")
