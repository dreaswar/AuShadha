################################################################################
# Project      : AuShadha
# Description  : Allergy Views
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
from allergy_list.models import Allergy, AllergyForm


# Views start here -----------------------------------------
@login_required
def allergy_list_json(request, patient_id = None):
    try:
      if patient_id:
        patient_id  = int(patient_id)
      else:
        action = unicode(request.GET.get('action'))
        patient_id = int(request.GET.get('patient_id'))

        if action == 'add':
            return allergy_list_add(request, patient_id)

      patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
      allergy_list_obj = Allergy.objects.filter(
          patient_detail=patient_detail_obj)
      json = generate_json_for_datagrid(allergy_list_obj)
      return HttpResponse(json, content_type="application/json")

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def allergy_list_add(request, patient_id = None):

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
          allergy_list_obj = Allergy(patient_detail=patient_detail_obj)
        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")
        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            allergy_list_form = AllergyForm( instance=allergy_list_obj)
            variable = RequestContext(request,
                                      {"user": user,
                                        "patient_detail_obj": patient_detail_obj,
                                        "allergy_list_form": allergy_list_form,
                                        "allergy_list_obj": allergy_list_obj,
                                        'addUrl' : p_urls['add']['allergy_list']
                                        })
            return render_to_response('allergy_list/add.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            allergy_list_form = AllergyForm(request.POST, 
                                                      instance=allergy_list_obj)
            if allergy_list_form.is_valid():
                allergy_list_obj = allergy_list_form.save()
                allergy_list_obj.generate_urls()
                m_urls = allergy_list_obj.urls
                print "Allergy URLS: "
                print m_urls
                patient_detail_obj.generate_urls()
                p_urls = patient_detail_obj.urls

                fields_list = [field for field in allergy_list_obj._meta.fields if field.serialize]

                success = True
                error_message = "Allergy Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(allergy_list_obj) for f in fields_list}
                addData['add'] = p_urls['add']['allergy_list']
                addData['json']= p_urls['json']['allergy_list']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(allergy_list_form)
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
def allergy_list_edit(request, allergy_list_id = None):

    if request.user:
        user = request.user
        try:
          allergy_list_id = int(allergy_list_id)
          allergy_list_obj = Allergy.objects.get(pk= allergy_list_id)
          allergy_list_obj.generate_urls()
          m_urls = allergy_list_obj.urls

        except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
        except Allergy.DoesNotExist:
            raise Http404("BadRequest: Patient Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            print "Received request for Editing Allergy"
            print "Allergy URLS is, ", m_urls
            allergy_list_form = AllergyForm(instance=allergy_list_obj)
            variable = RequestContext(request,
                                      { "user": user,
                                        "patient_detail_obj"  : allergy_list_obj.patient_detail,
                                        "allergy_list_form": allergy_list_form,
                                        "allergy_list_obj" : allergy_list_obj,
                                        'editUrl'            : m_urls['edit'],
                                        'delUrl'             : m_urls['del'],
                                      })
            return render_to_response('allergy_list/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            allergy_list_form = AllergyForm(request.POST, 
                                                           instance=allergy_list_obj)

            if allergy_list_form.is_valid():
                allergy_list_obj = allergy_list_form.save()

                allergy_list_obj.generate_urls()
                m_urls = allergy_list_obj.urls

                allergy_list_obj.patient_detail.generate_urls()
                p_urls = allergy_list_obj.patient_detail.urls

                fields_list = [field for field in allergy_list_obj._meta.fields if field.serialize]

                success = True
                error_message = "Allergy Data Edited Successfully"
                form_errors = None

                addData = {f.name:f.value_to_string(allergy_list_obj) for f in fields_list}
                addData['add'] = p_urls['add']['allergy_list']
                addData['json']= p_urls['json']['allergy_list']
                addData['edit']= m_urls['edit']
                addData['del'] = m_urls['del']

            else:
                success = False
                error_message = aumodelformerrorformatter_factory(allergy_list_form)
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
def allergy_list_del(request, allergy_list_id = None):
    user = request.user

    if request.user and user.is_superuser:

        if request.method == "GET":

            try:
                if allergy_list_id: 
                  allergy_list_id = int(allergy_list_id)
                else:
                  allergy_list_id = int(request.GET.get('allergy_list_id'))
                allergy_list_obj = Allergy.objects.get(pk=allergy_list_id)
                patient_detail_obj = allergy_list_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Allergy.DoesNotExist:
                raise Http404(
                    "BadRequest: Allergy Data Does Not Exist")

            allergy_list_obj.delete()
            success = True
            error_message = "Allergy Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")

    else:
        raise Http404("Server Error: No Permission to delete.")
