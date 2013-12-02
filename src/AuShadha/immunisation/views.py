################################################################################
# Project      : AuShadha
# Description  : Immunisation Views
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

from patient.models import PatientDetail

#patient = UI.registry.get('PatientRegistration','')
#if patient:
  #print "UI has PatientRegistration role and class defined"
  #module = importlib.import_module(patient.__module__)
  #PatientDetail = getattr(module, patient.__name__)
#else:
  #raise Exception("""
                  #PatientRegistration role not defined and hence cannot be imported.
                  #This module depends on this. 
                  #Please register the module and class for PatientRegistration Role
                  #"""
                  #)

from immunisation.models import Immunisation, ImmunisationForm


# Views start here -----------------------------------------
@login_required
def immunisation_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id  = int(patient_id)
      else:
        action = unicode(request.GET.get('action'))
        patient_id = int(request.GET.get('patient_id'))

        if action == 'add':
            return immunisation_add(request, patient_id)

      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      immunisation_obj = Immunisation.objects.filter(
          patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(immunisation_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def immunisation_add(request, patient_id = None):

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
          immunisation_obj = Immunisation(patient_detail=patient_detail_obj)
        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")
        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            immunisation_form = ImmunisationForm( instance=immunisation_obj, auto_id = False )
            variable = RequestContext(request,
                                      {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "immunisation_form": immunisation_form,
                                        "immunisation_obj": immunisation_obj,
                                        'addUrl' : p_urls['add']['immunisation']
                                        })
            return render_to_response('immunisation/add.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            immunisation_form = ImmunisationForm(request.POST, 
                                                      instance=immunisation_obj)
            if immunisation_form.is_valid():
                immunisation_obj = immunisation_form.save()
                immunisation_obj.generate_urls()
                m_urls = immunisation_obj.urls
                print "Immunisation URLS: "
                print m_urls
                patient_detail_obj.generate_urls()
                p_urls = patient_detail_obj.urls

                fields_list = [field for field in immunisation_obj._meta.fields if field.serialize]

                success = True
                error_message = "Immunisation Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(immunisation_obj) for f in fields_list}
                addData['add'] = p_urls['add']['immunisation']
                addData['json']= p_urls['json']['immunisation']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(immunisation_form)
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
def immunisation_edit(request, immunisation_id = None):

    if request.user:
        user = request.user
        try:
          immunisation_id = int(immunisation_id)
          immunisation_obj = Immunisation.objects.get(pk= immunisation_id)
          immunisation_obj.generate_urls()
          m_urls = immunisation_obj.urls

        except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
        except Immunisation.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            print "Received request for Editing Immunisation"
            print "Immunisation URLS is, ", m_urls
            immunisation_form = ImmunisationForm(instance=immunisation_obj, auto_id = False )
            variable = RequestContext(request,
                                      { "user": user,
                                        "patient_detail_obj"  : immunisation_obj.patient_detail,
                                        "immunisation_form": immunisation_form,
                                        "immunisation_obj" : immunisation_obj,
                                        'editUrl'            : m_urls['edit'],
                                        'delUrl'             : m_urls['del'],
                                      })
            return render_to_response('immunisation/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            immunisation_form = ImmunisationForm(request.POST, 
                                                           instance=immunisation_obj)

            if immunisation_form.is_valid():
                immunisation_obj = immunisation_form.save()

                immunisation_obj.generate_urls()
                m_urls = immunisation_obj.urls

                immunisation_obj.patient_detail.generate_urls()
                p_urls = immunisation_obj.patient_detail.urls

                fields_list = [field for field in immunisation_obj._meta.fields if field.serialize]

                success = True
                error_message = "Immunisation Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(immunisation_obj) for f in fields_list}
                addData['add'] = p_urls['add']['immunisation']
                addData['json']= p_urls['json']['immunisation']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(immunisation_form)
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
def immunisation_del(request, immunisation_id = None):
    user = request.user

    if request.user and user.is_superuser:

        if request.method == "GET":

            try:
                if immunisation_id: 
                  immunisation_id = int(immunisation_id)
                else:
                  immunisation_id = int(request.GET.get('immunisation_id'))
                immunisation_obj = Immunisation.objects.get(pk=immunisation_id)
                patient_detail_obj = immunisation_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Immunisation.DoesNotExist:
                raise Http404(
                    "BadRequest: Immunisation Data Does Not Exist")

            immunisation_obj.delete()
            success = True
            error_message = "Immunisation Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")
