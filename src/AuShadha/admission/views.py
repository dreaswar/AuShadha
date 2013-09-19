################################################################################
# Project     : AuShadha
# Description : Views for Patient Admission
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 18-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder



# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from core.serializers.data_grid import generate_json_for_datagrid

from patient.models import PatientDetail, PatientDetailForm
from admission.models import Admission

#from clinic.models import Clinic
#from demographics.models import Contact, Phone, Guardian, Demographics
#from medical_history.models import MedicalHistory
#from surgical_history.models import SurgicalHistory
#from social_history.models import SocialHistory
#from family_history.models import FamilyHistory
#from immunisation.models import Immunisation
#from allergy_list.models import Allergy
#from medication_list.models import MedicationList
#from admission.models import Admission, AdmissionForm
#from visit.models import VisitDetail, VisitImaging, VisitInv
#from obs_and_gyn.models import ObstetricHistoryDetail


# Views start here -----------------------------------------

@login_required
def admission_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return patient_admission_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")
    patient_admission_obj = Admission.objects.filter(
        patient_detail=patient_detail_obj)
    data = []
    if patient_admission_obj:
        for admission in patient_admission_obj:
            data_to_append = {}
            data_to_append['id'] = admission.id
            data_to_append[
                'date_of_admission'] = admission.date_of_admission.isoformat()
            data_to_append[
                'time_of_admission'] = admission.time_of_admission.isoformat()
            data_to_append[
                'admitting_surgeon'] = admission.admitting_surgeon.surgeon_name
            data_to_append['room_or_ward'] = admission.room_or_ward
            data_to_append['admission_closed'] = admission.admission_closed
            data_to_append['hospital'] = admission.hospital
            data_to_append[
                'home'] = admission.get_admission_main_window_url()
            data_to_append[
                'edit'] = admission.get_admission_edit_url()
            data_to_append[
                'del'] = admission.get_admission_del_url()
            data.append(data_to_append)
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")

@login_required
def admission_add(request, id=None):

    if request.is_ajax():

        if request.user:
            user = request.user

            if request.method == 'GET':
                get_data = request.GET.copy()
                try:
                    if not id:
                        patient_id = int(request.GET.get('patient_id'))
                    else:
                        patient_id = int(id)
                    patient_obj = PatientDetail.objects.get(pk=patient_id)
                except(ValueError, TypeError, KeyError, AttributeError):
                    message = '''
                             Server Error !!. Invalid Request parameters.
                             Please check your request and try again..
                           '''
                    return HttpResponse(message)
                except(PatientDetail.DoesNotExist):
                    return HttpResponse("Bad Request. The requested patient data does not exist.")

                all_admissions = Admission.objects.filter(
                    patient_detail=patient_obj).filter(admission_closed=False)

                if len(all_admissions) > 0:
                    error_message = "Admission is still active. Cannot add more"
                    admission_add_form = None
                    adm_obj = None
                else:
                    error_message = None
                    adm_obj = Admission(
                        patient_detail=patient_obj)
                    admission_add_form = AdmissionForm(
                        instance=adm_obj)
                    print 'received GET for patient with id ' + str(patient_id)
                variable = RequestContext(request,
                                          {'user': user,
                                           'admission_add_form': admission_add_form,
                                           'patient_detail_obj': patient_obj,
                                           'adm_obj': adm_obj,
                                           'error_message': error_message
                                           })
                return render_to_response('admission/detail/add.html', variable)
            elif request.method == "POST":
                try:
                    if not id:
                        patient_id = int(request.POST['patient_id'])
                    else:
                        patient_id = int(id)
                    patient_obj = PatientDetail.objects.get(
                        pk=patient_id)
                except(ValueError, TypeError, KeyError, AttributeError):
                    raise Http404("Bad Request. Invalid Request Parameters.")
                except(PatientDetail.DoesNotExist):
                    raise Http404(
                        "Bad Request. The requested patient data does not exist.")
                adm_obj = Admission(
                    patient_detail=patient_obj)
                request_post_copy = request.POST.copy()
                time = request.POST.get(
                    'time_of_admission')[1:]
                request_post_copy['time_of_admission'] = time
                patient_admission_add_form = AdmissionForm(
                    request_post_copy, instance=adm_obj)
                print request.POST
                if patient_obj.has_active_admission() != '0':
                    error_message   =  '''
                                        This patient has an active Admission. 
                                        You cannot add admission now.
                                     '''
                    success = False
                    form_errors = patient_admission_add_form.errors
                else:
                    if patient_admission_add_form.is_valid():
                        saved_adm_obj = patient_admission_add_form.save()
                        print "DATE OF ADMISSION IS:: " + saved_adm_obj.date_of_admission.isoformat()
                        print "TIME OF ADMISSION IS:: " + saved_adm_obj.time_of_admission.isoformat()
                        error_message = 'Admission added successfully'
                        success = True
                        form_errors = patient_admission_add_form.errors
                        data = {
                            'error_message': error_message,
                            'success': success,
                            'form_errors': form_errors,
                            'id': saved_adm_obj.id,
                            'date_of_admission': saved_adm_obj.date_of_admission.isoformat(),
                            'time_of_admission': saved_adm_obj.time_of_admission.isoformat(),
                            'admission_closed': saved_adm_obj.admission_closed,
                            'admitting_surgeon': saved_adm_obj.admitting_surgeon.surgeon_name,
                            'hospital': saved_adm_obj.hospital,
                            'room_or_ward': saved_adm_obj.room_or_ward,
                            'home': saved_adm_obj.get_admission_main_window_url(),
                            'edit': saved_adm_obj.get_admission_edit_url(),
                            'del': saved_adm_obj.get_admission_del_url()
                        }
                        json = simplejson.dumps(data)
                        return HttpResponse(json, content_type='application/json')
                    else:
                        error_message   = '''
                                           Error ! Admission could not be added:
                                           Submitted Data Did not validate.
                                        '''
                        success = False
                        form_errors = patient_admission_add_form.errors
                        print form_errors
                data = {
                    'error_message': error_message,
                    'success': success,
                    'form_errors': form_errors
                }
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')
            else:
                return HttpResponse('Invalid Request')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render_to_response('admission/detail/add.html', variable)