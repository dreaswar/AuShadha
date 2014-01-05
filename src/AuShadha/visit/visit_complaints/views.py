#################################################################################
# Project     : AuShadha
# Description : AuShadha Views for OPD Visits
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
from django.utils import simplejson

# General Module imports-----------------------------------
from datetime import datetime, date, time
import xhtml2pdf.pisa as pisa
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

from .models import VisitComplaint, VisitComplaintAddForm, VisitComplaintEditForm
from .utilities import check_duplicates

# views start here;;


@login_required
def visit_complaint_json(request, visit_id = None):

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

    #visit_complaint_objs  = []
    #all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    #for visit in all_visits:
      #vc = VisitComplaint.objects.filter(visit_detail = visit)
      #for c in vc:
        #visit_complaint_objs.append(c)

    visit_complaint_objs = VisitComplaint.objects.filter(visit_detail = visit_detail_obj)
    data = []

    if visit_complaint_objs:
        for complaint in visit_complaint_objs:
            if not getattr(complaint, 'urls', None):
              complaint.save()
            i = 0
            data_to_append = {}
            data_to_append['id'] = complaint.id
            data_to_append['complaint'] = complaint.complaint
            data_to_append['duration'] = complaint.duration
            data_to_append['edit'] = complaint.urls['edit']
            data_to_append['del'] = complaint.urls['del']
            data.append(data_to_append)
            i += 1

    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")



@login_required
def visit_complaint_add(request, visit_id = None):

    """ 
    Adds a Visit complaint
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
        visit_complaint_obj = VisitComplaint(visit_detail=visit_detail_obj)

        if not getattr(patient_detail_obj, 'urls', None):
          patient_detail_obj.save()

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()

        if request.method == "GET" and request.is_ajax():

            visit_complaint_form = VisitComplaintAddForm(instance = visit_complaint_obj,
                                                      auto_id  =
                                                      "id_add_visit_complaint"+
                                                      str(visit_id)+"_%s")
            variable = RequestContext(request, {
                                                'user': user,
                                                'visit_detail_obj': visit_detail_obj,
                                                'visit_complaint_form': visit_complaint_form,
                                                'patient_detail_obj': patient_detail_obj,
                                                'error_message': error_message,
                                                'success': success,
                                            })

            return render_to_response('visit_complaints/forms/add.html', variable)

        elif request.method == "POST" and request.is_ajax():

            visit_complaint_form = VisitComplaintAddForm(request.POST, instance = visit_complaint_obj)

            if visit_complaint_form.is_valid() :
                saved_visit_complaint = visit_complaint_form.save(commit=False)
                saved_visit_complaint.visit_detail = visit_detail_obj

                if check_duplicates(saved_visit_complaint, visit_detail_obj):
                    saved_visit_complaint.save()
                    success = True
                    error_message = "Visit Added Successfully"

                else:
                    success = False
                    error_message = ''' <h4>
                                        Visit Could not be Saved as there are duplicate complaints.
                                        Please check the forms for errors
                                        </h4>
                                    '''

            else:
                error_message = ''' <h4>
                                      Visit Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_complaint_form)
                error_message += ('\n' + errors)

            data = {'success': success,
                    'error_message': error_message
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")


@login_required
def visit_complaint_edit(request, visit_complaint_id = None):

    user = request.user
    error_message = None    
    
    try:

        if visit_complaint_id:
          visit_complaint_id = int(visit_complaint_id)

        else:
          visit_complaint_id = int(request.GET.get('visit_complaint_id'))

        visit_complaint_obj = VisitComplaint.objects.get(pk=visit_complaint_id)
        visit_detail_obj = visit_complaint_obj.visit_detail
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        if not getattr(patient_detail_obj,'urls',None):
          patient_detail_obj.save()

        if not getattr(visit_complaint_obj,'urls',None):
          visit_complaint_obj.save()
        
        if request.method == "GET" and request.is_ajax():

            visit_complaint_form = VisitComplaintEditForm(instance = visit_complaint_obj, 
                                                          auto_id = False
                                                        )

            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_complaint_obj': visit_complaint_obj,
                          'visit_complaint_form'  : visit_complaint_form  ,
                          'patient_detail_obj': visit_detail_obj.patient_detail,
                          'error_message': error_message,
                          'form_action':'edit'
                          })

            return render_to_response('visit_complaints/forms/edit.html', variable)

        if request.method == "POST" and request.is_ajax():

            visit_complaint_form   = VisitComplaintEditForm(request.POST, instance = visit_complaint_obj )

            if visit_complaint_form.is_valid():

                saved_visit_complaint = visit_complaint_form.save(commit=False)
                saved_visit_complaint.visit_detail = visit_detail_obj

                if check_duplicates(saved_visit_complaint, visit_detail_obj):
                    saved_visit_complaint.save()
                    success = True
                    error_message = "Visit Edited Successfully"

                else:
                    success = False
                    error_message = ''' <h4>
                                        Visit Could not be Saved as there are duplicate complaints.
                                        Please check the forms for errors
                                        </h4>
                                    '''

            else:
                success = False
                error_message = ''' <h4>
                                      Visit Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_complaint_form)
                error_message += ('\n' + errors)

            data = {'success': success, 'error_message': error_message }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
             raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitComplaint.DoesNotExist):
        raise Http404("Requested VisitComplaint Does not exist.")


@login_required
def visit_complaint_del(request, visit_complaint_id = None):

    if request.method == "GET" and request.is_ajax():

        user = request.user

        try:

            if visit_complaint_id:
              visit_complaint_id = int(visit_complaint_id)

            else:
              visit_complaint_id = int(request.GET.get('visit_complaint_id'))

            visit_complaint_obj = VisitComplaint.objects.get(pk=visit_complaint_id)
            error_message = None
            visit_complaint_obj.delete()
            success = True
            error_message = "Successfully Deleted Visit Complaint "
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitComplaint.DoesNotExist):
            raise Http404("Requested Visit Complaint Does not exist.")

    else:
        raise Http404(" Error ! Unsupported Request..")