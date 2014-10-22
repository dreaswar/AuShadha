#################################################################################
# Project     : AuShadha
# Description : AuShadha Views for OPD Visits History
# Author      : Dr.Easwar T.R 
# Date        : 27-12-2012
# License     : GNU - GPL Version 3, see AuShadha/LICENSE.txt
#################################################################################


# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
#from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator
import json

# General Module imports-----------------------------------
from datetime import datetime, date, time
#import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from collections import OrderedDict
import importlib

# Application Specific Model Imports-----------------------
from AuShadha.utilities.forms import AuModelFormErrorFormatter, aumodelformerrorformatter_factory
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.aushadha_users.models import AuShadhaUser
from AuShadha.apps.clinic.models import Clinic, Staff
from AuShadha.apps.ui.ui import ui as UI

from registry.inv_and_imaging.models import LabInvestigationRegistry, ImagingInvestigationRegistry

#from patient.models import PatientDetail
#from admission.models import AdmissionDetail
PatientDetail = UI.get_module('PatientRegistration')
AdmissionDetail = UI.get_module('Admission')
VisitDetail = UI.get_module('OPD_Visit')

from .models import VisitHPI, VisitHPIForm


# views start here;;


@login_required
def visit_hpi_json(request, visit_id = None):

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))          

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()
    
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    
    except(VisitDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")

    #visit_hpi_objs  = []
    #all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    #for visit in all_visits:
      #vc = VisitHPI.objects.filter(visit_detail = visit)
      #for c in vc:
        #visit_hpi_objs.append(c)

    visit_hpi_objs = VisitHPI.objects.filter(visit_detail = visit_detail_obj)
    data = []

    if visit_hpi_objs:
        for hpi in visit_hpi_objs:
            if not getattr(hpi, 'urls', None):
              hpi.save()
            i = 0
            data_to_append = {}
            data_to_append['id'] = hpi.id
            data_to_append['hpi'] = hpi.hpi
            data_to_append['edit'] = hpi.urls['edit']
            data_to_append['del'] = hpi.urls['del']
            data.append(data_to_append)
            i += 1

    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type="application/json")



@login_required
def visit_hpi_add(request, visit_id = None):

    """ 
    Adds a Visit hpi
    """

    user = request.user
    success = False
    error_message = None
    form_errors = []

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(patient_detail_obj, 'urls', None):
          patient_detail_obj.save()

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()

        visit_hpi_objs = VisitHPI.objects.filter(visit_detail = visit_detail_obj)
        if visit_hpi_objs:
          return visit_hpi_edit(request, visit_hpi_id = visit_hpi_objs[0].id)

        visit_hpi_obj = VisitHPI(visit_detail=visit_detail_obj)

        if request.method == "GET" and request.is_ajax():

            visit_hpi_form = VisitHPIForm(instance = visit_hpi_obj,
                                                      auto_id  = "id_add_visit_hpi"+ str(visit_id)+"_%s")
            variable = RequestContext(request, {
                                                'user': user,
                                                'visit_detail_obj': visit_detail_obj,
                                                'visit_hpi_form': visit_hpi_form,
                                                'patient_detail_obj': patient_detail_obj,
                                                'error_message': error_message,
                                                'success': success,
                                                'visit_hpi_action':'add'
                                            })

            return render_to_response('visit_hpi/add_or_edit_form.html', variable)

        elif request.method == "POST" and request.is_ajax():

            visit_hpi_form = VisitHPIForm(request.POST, instance = visit_hpi_obj)

            if visit_hpi_form.is_valid() :
                saved_visit_hpi = visit_hpi_form.save(commit=False)
                saved_visit_hpi.visit_detail = visit_detail_obj
                saved_visit_hpi.save()
                success = True
                error_message = "History Added Successfully"
                redirectUrl = saved_visit_hpi.urls['edit']

            else:
                error_message = ''' <h4>
                                      History Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_hpi_form)
                error_message += ('\n' + errors)
                redirectUrl = None
                success = False

            data = {'success': success,
                    'error_message': error_message,
                    'redirectUrl': redirectUrl
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")


@login_required
def visit_hpi_edit(request, visit_hpi_id = None):

    user = request.user
    error_message = None    
    
    try:

        if visit_hpi_id:
          visit_hpi_id = int(visit_hpi_id)

        else:
          visit_hpi_id = int(request.GET.get('visit_hpi_id'))

        visit_hpi_obj = VisitHPI.objects.get(pk=visit_hpi_id)
        visit_detail_obj = visit_hpi_obj.visit_detail
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        if not getattr(patient_detail_obj,'urls',None):
          patient_detail_obj.save()

        if not getattr(visit_hpi_obj,'urls',None):
          visit_hpi_obj.save()
        
        if request.method == "GET" and request.is_ajax():

            visit_hpi_form = VisitHPIForm(instance = visit_hpi_obj, 
                                          auto_id = "id_edit_visit_hpi"+ str(visit_hpi_id)+"_%s"
                                          )

            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_hpi_obj': visit_hpi_obj,
                          'visit_hpi_form'  : visit_hpi_form  ,
                          'patient_detail_obj': visit_detail_obj.patient_detail,
                          'error_message': error_message,
                          'visit_hpi_action':'edit'
                          })

            return render_to_response('visit_hpi/add_or_edit_form.html', variable)

        if request.method == "POST" and request.is_ajax():

            visit_hpi_form   = VisitHPIForm(request.POST, instance = visit_hpi_obj )

            if visit_hpi_form.is_valid()    :                

                saved_visit_hpi = visit_hpi_form.save(commit=False)
                saved_visit_hpi.visit_detail = visit_detail_obj
                saved_visit_hpi.save()
                success = True
                error_message = "Visit History Edited Successfully"
                redirectUrl = saved_visit_hpi.urls['edit']

            else:
                success = False
                error_message = ''' <h4>
                                      Visit Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_hpi_form)
                error_message += ('\n' + errors)
                redirectUrl = None

            data = {'success': success, 'error_message': error_message , 'redirectUrl': redirectUrl }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        else:
             raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitHPI.DoesNotExist):
        raise Http404("Requested VisitHPI Does not exist.")


@login_required
def visit_hpi_del(request, visit_hpi_id = None):
    
    if request.method == "GET" and request.is_ajax():

        user = request.user

        try:
            if visit_hpi_id:
              visit_hpi_id = int(visit_hpi_id)
            else:
              visit_hpi_id = int(request.GET.get('visit_hpi_id'))

            visit_hpi_obj = VisitHPI.objects.get(pk=visit_hpi_id)
            visit_detail_obj = visit_hpi_obj.visit_detail

            if not getattr(visit_detail_obj,'urls', None):
              visit_detail_obj.save()

            visit_hpi_obj.delete()
            error_message = None
            success = True
            error_message = "Successfully Deleted Visit History "
            data = {'success': success, 
                    'error_message': error_message, 
                    'redirectUrl': visit_detail_obj.urls['add']['visit_hpi'] 
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitHPI.DoesNotExist):
            raise Http404("Requested Visit History Does not exist.")

    else:
        raise Http404(" Error ! Unsupported Request..")