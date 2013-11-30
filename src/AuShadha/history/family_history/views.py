################################################################################
# Project      : AuShadha
# Description  : Family History Views
# Author       : Dr.Easwar T.R 
# Date         : 16-09-2013
# License      : GNU-GPL Version 3,Please see AuShadha/LICENSE.txt for details
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time
import importlib

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
from AuShadha.apps.ui.ui import ui as UI

#from patient.models import PatientDetail

patient = UI.registry.get('PatientRegistration','')
if patient:
  print "UI has PatientRegistration role and class defined"
  module = importlib.import_module(patient.__module__)
  PatientDetail = getattr(module, patient.__name__)
else:
  raise Exception("""
                  PatientRegistration role not defined and hence cannot be imported.
                  This module depends on this. 
                  Please register the module and class for PatientRegistration Role
                  """
                  )

from history.family_history.models import FamilyHistory, FamilyHistoryForm


# Views start here -----------------------------------------
@login_required
def family_history_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id  = int(patient_id)
      else:
        action = unicode(request.GET.get('action'))
        patient_id = int(request.GET.get('patient_id'))

        if action == 'add':
            return family_history_add(request, patient_id)

      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      family_history_obj = FamilyHistory.objects.filter(
          patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(family_history_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def family_history_add(request, patient_id = None):

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
          family_history_obj = FamilyHistory(patient_detail=patient_detail_obj)
        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")
        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            family_history_form = FamilyHistoryForm( instance=family_history_obj, auto_id = False )
            variable = RequestContext(request,
                                      {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "family_history_form": family_history_form,
                                        "family_history_obj": family_history_obj,
                                        'addUrl' : p_urls['add']['family_history']
                                        })
            return render_to_response('family_history/add.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            family_history_form = FamilyHistoryForm(request.POST, 
                                                      instance=family_history_obj)
            if family_history_form.is_valid():
                family_history_obj = family_history_form.save()
                family_history_obj.generate_urls()
                m_urls = family_history_obj.urls
                print "Family History URLS: "
                print m_urls
                patient_detail_obj.generate_urls()
                p_urls = patient_detail_obj.urls

                fields_list = [field for field in family_history_obj._meta.fields if field.serialize]

                success = True
                error_message = "Family History Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(family_history_obj) for f in fields_list}
                addData['add'] = p_urls['add']['family_history']
                addData['json']= p_urls['json']['family_history']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(family_history_form)
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
def family_history_edit(request, family_history_id = None):

    if request.user:
        user = request.user
        try:
          family_history_id = int(family_history_id)
          family_history_obj = FamilyHistory.objects.get(pk= family_history_id)
          family_history_obj.generate_urls()
          m_urls = family_history_obj.urls

        except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
        except FamilyHistory.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            print "Received request for Editing Family History"
            print "Family History URLS is, ", m_urls
            family_history_form = FamilyHistoryForm(instance=family_history_obj, auto_id = False )
            variable = RequestContext(request,
                                      { "user": user,
                                        "patient_detail_obj"  : family_history_obj.patient_detail,
                                        "family_history_form": family_history_form,
                                        "family_history_obj" : family_history_obj,
                                        'editUrl'            : m_urls['edit'],
                                        'delUrl'             : m_urls['del'],
                                      })
            return render_to_response('family_history/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            family_history_form = FamilyHistoryForm(request.POST, 
                                                           instance=family_history_obj)

            if family_history_form.is_valid():
                family_history_obj = family_history_form.save()

                family_history_obj.generate_urls()
                m_urls = family_history_obj.urls

                family_history_obj.patient_detail.generate_urls()
                p_urls = family_history_obj.patient_detail.urls

                fields_list = [field for field in family_history_obj._meta.fields if field.serialize]

                success = True
                error_message = "Family History Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(family_history_obj) for f in fields_list}
                addData['add'] = p_urls['add']['family_history']
                addData['json']= p_urls['json']['family_history']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(family_history_form)
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
def family_history_del(request, family_history_id = None):
    user = request.user

    if request.user and user.is_superuser:

        if request.method == "GET":

            try:
                if family_history_id: 
                  family_history_id = int(family_history_id)
                else:
                  family_history_id = int(request.GET.get('family_history_id'))
                family_history_obj = FamilyHistory.objects.get(pk=family_history_id)
                patient_detail_obj = family_history_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except FamilyHistory.DoesNotExist:
                raise Http404(
                    "BadRequest: Family History Data Does Not Exist")

            family_history_obj.delete()
            success = True
            error_message = "Family History Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")
