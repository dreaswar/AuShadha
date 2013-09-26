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

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory

from patient.models import PatientDetail
from medical_history.models import MedicalHistory, MedicalHistoryForm


# Views start here -----------------------------------------
@login_required
def medical_history_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id  = int(patient_id)
      else:
        action = unicode(request.GET.get('action'))
        patient_id = int(request.GET.get('patient_id'))

        if action == 'add':
            return medical_history_add(request, patient_id)

      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      medical_history_obj = MedicalHistory.objects.filter(
          patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(medical_history_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def medical_history_add(request, patient_id = None):

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
          medical_history_obj = MedicalHistory(patient_detail=patient_detail_obj)
        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")
        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            medical_history_form = MedicalHistoryForm( instance=medical_history_obj)
            variable = RequestContext(request,
                                      {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "medical_history_form": medical_history_form,
                                        "medical_history_obj": medical_history_obj,
                                        'addUrl' : p_urls['add']['medical_history']
                                        })
            return render_to_response('medical_history/add.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            medical_history_form = MedicalHistoryForm(request.POST, 
                                                      instance=medical_history_obj)
            if medical_history_form.is_valid():
                medical_history_obj = medical_history_form.save()
                medical_history_obj.generate_urls()
                m_urls = medical_history_obj.urls
                print "Medical History URLS: "
                print m_urls
                patient_detail_obj.generate_urls()
                p_urls = patient_detail_obj.urls

                fields_list = [field for field in medical_history_obj._meta.fields if field.serialize]

                success = True
                error_message = "Medical History Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(medical_history_obj) for f in fields_list}
                addData['add'] = p_urls['add']['medical_history']
                addData['json']= p_urls['json']['medical_history']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(medical_history_form)
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
def medical_history_edit(request, medical_history_id = None):

    if request.user:
        user = request.user
        try:
          medical_history_id = int(medical_history_id)
          medical_history_obj = MedicalHistory.objects.get(pk= medical_history_id)
          medical_history_obj.generate_urls()
          m_urls = medical_history_obj.urls

        except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
        except MedicalHistory.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            print "Received request for Editing Medical History"
            print "Medical History URLS is, ", m_urls
            medical_history_form = MedicalHistoryForm(instance=medical_history_obj)
            variable = RequestContext(request,
                                      { "user": user,
                                        "patient_detail_obj"  : medical_history_obj.patient_detail,
                                        "medical_history_form": medical_history_form,
                                        "medical_history_obj" : medical_history_obj,
                                        'editUrl'            : m_urls['edit'],
                                        'delUrl'             : m_urls['del'],
                                      })
            return render_to_response('medical_history/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            medical_history_form = MedicalHistoryForm(request.POST, 
                                                           instance=medical_history_obj)

            if medical_history_form.is_valid():
                medical_history_obj = medical_history_form.save()

                medical_history_obj.generate_urls()
                m_urls = medical_history_obj.urls

                medical_history_obj.patient_detail.generate_urls()
                p_urls = medical_history_obj.patient_detail.urls

                fields_list = [field for field in medical_history_obj._meta.fields if field.serialize]

                success = True
                error_message = "Medical History Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(medical_history_obj) for f in fields_list}
                addData['add'] = p_urls['add']['medical_history']
                addData['json']= p_urls['json']['medical_history']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(medical_history_form)
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
def medical_history_del(request, medical_history_id = None):
    user = request.user

    if request.user and user.is_superuser:

        if request.method == "GET":

            try:
                if medical_history_id: 
                  medical_history_id = int(medical_history_id)
                else:
                  medical_history_id = int(request.GET.get('medical_history_id'))
                medical_history_obj = MedicalHistory.objects.get(pk=medical_history_id)
                patient_detail_obj = medical_history_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except MedicalHistory.DoesNotExist:
                raise Http404(
                    "BadRequest: Medical History Data Does Not Exist")

            medical_history_obj.delete()
            success = True
            error_message = "Medical History Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")
