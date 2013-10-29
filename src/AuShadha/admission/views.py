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
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid

from patient.models import PatientDetail, PatientDetailForm
from .models import AdmissionDetail,AdmissionDetailForm, \
                    AdmissionHPI, AdmissionROS, AdmissionImaging, \
                    AdmissionInv, AdmissionComplaint

from dijit_widgets.tree import AdmissionTree
from AuShadha.apps.ui.data.json import ModelInstanceJson

from demographics.demographics.models import Demographics
from demographics.contact.models import Contact
from demographics.phone.models import Phone
from demographics.guardian.models import Guardian
from demographics.email_and_fax.models import EmailAndFax

from history.social_history.models import SocialHistory
from history.family_history.models import FamilyHistory
from history.medical_history.models import MedicalHistory
from history.surgical_history.models import SurgicalHistory
#from history.obs_and_gyn.models import ObstetricHistoryDetail

from medication_list.models import MedicationList
from allergy_list.models import Allergy

from registry.inv_and_imaging.models import LabInvestigationRegistry, ImagingInvestigationRegistry

from phyexam.models import *
from phyexam.models import DEFAULT_VITALS

from phyexam.presentation_classes import VitalExamObjPresentationClass,\
                                         GenExamObjPresentationClass,\
                                         SysExamObjPresentationClass,\
                                         vitalexamobjpresentationclass_factory,\
                                         genexamobjpresentationclass_factory,\
                                         sysexamobjpresentationclass_factory,\
                                         neuroexamobjpresentationclass_factory,\
                                         vascexamobjpresentationclass_factory,\
                                         vascexamobjpresentationclass_querysetfactory,\
                                         visitrospresentationclass_factory



# Views start here -----------------------------------------

@login_required
def render_admission_json(request):

    if request.method =='GET':
      all_a = AdmissionDetail.objects.all()
      if all_a is not None:
          data = []
          for admission in all_a:
              print "Evaluating Admission.. "
              print admission
              json = ModelInstanceJson(admission).return_data()
              data.append(json)
      else:
        data = {}
      json = simplejson.dumps(data)
      print "\n"
      print "-" *100
      print "Printing Sample Admission JSON"
      print "-" *100
      if data: 
        print (simplejson.dumps(data[0]))
      else:
        print "No Admissions"
      print "-" *100
      print "\n"
      return HttpResponse(json, content_type="application/json")
    else:
      raise Http404("Bad Request Method")


#@login_required
#def admission_json(request):
    #try:
        #action = unicode(request.GET.get('action'))
        #id = int(request.GET.get('patient_id'))
        #if action == 'add':
            #return patient_admission_add(request, id)
        #patient_detail_obj = PatientDetail.objects.get(pk=id)
    #except(AttributeError, NameError, TypeError, ValueError, KeyError):
        #raise Http404("ERROR:: Bad request.Invalid arguments passed")
    #except(PatientDetail.DoesNotExist):
        #raise Http404("ERROR:: Patient requested does not exist.")
    #patient_admission_obj = Admission.objects.filter(
        #patient_detail=patient_detail_obj)
    #data = []
    #if patient_admission_obj:
        #for admission in patient_admission_obj:
            #data_to_append = {}
            #data_to_append['id'] = admission.id
            #data_to_append[
                #'date_of_admission'] = admission.date_of_admission.isoformat()
            #data_to_append[
                #'time_of_admission'] = admission.time_of_admission.isoformat()
            #data_to_append[
                #'admitting_surgeon'] = admission.admitting_surgeon.surgeon_name
            #data_to_append['room_or_ward'] = admission.room_or_ward
            #data_to_append['admission_closed'] = admission.admission_closed
            #data_to_append['hospital'] = admission.hospital
            #data_to_append[
                #'home'] = admission.get_admission_main_window_url()
            #data_to_append[
                #'edit'] = admission.get_admission_edit_url()
            #data_to_append[
                #'del'] = admission.get_admission_del_url()
            #data.append(data_to_append)
    #json = simplejson.dumps(data)
    #return HttpResponse(json, content_type="application/json")


@login_required
def render_admission_tree(request, patient_id=None):
    if request.method == "GET" and request.is_ajax():
      tree = AdmissionTree(request)()
      return HttpResponse(tree, content_type="application/json")
    else:
        raise Http404("Bad Request")



@login_required
def admission_summary(request, patient_id = None):

    user = request.user

    if request.method == "GET" and request.is_ajax():
        try:
            if patient_id:
              patient_id = int(patient_id)
            else:
              patient_id = int(request.GET.get('patient_id') )
            print "Listing Summary for patient with ID: " + str(patient_id)
            patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
            admission_detail_obj = AdmissionDetail.objects.filter(
                patient_detail=patient_detail_obj).order_by('-date_of_admission')
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (PatientDetail.DoesNotExist):
            raise Http404("Requested Patient Does not exist.")

        admission_obj_list = []
        if admission_detail_obj:
            error_message = "Listing the Admissions in ", admission_detail_obj
            print "Listing the Admissions in ", admission_detail_obj
            for admission in admission_detail_obj:
                dict_to_append = OrderedDict()
                dict_to_append[admission] = None
                print "Aggregating sub-modules in admission: ", admission
                admission_complaint_obj = AdmissionComplaint.objects.filter(
                    admission_detail=admission)
                admission_hpi_obj = AdmissionHPI.objects.filter(
                    admission_detail=admission)
                admission_ros_obj = AdmissionROS.objects.filter(
                    admission_detail=admission)
                vital_exam_obj = VitalExam_FreeModel.objects.filter(
                    admission_detail=admission)
                gen_exam_obj = GenExam_FreeModel.objects.filter(
                    admission_detail=admission)
                sys_exam_obj = SysExam_FreeModel.objects.filter(
                    admission_detail=admission)
                neuro_exam_obj = PeriNeuroExam_FreeModel.objects.filter(
                    admission_detail=admission)
                vasc_exam_obj = VascExam_FreeModel.objects.filter(
                    admission_detail=admission)

                if admission_hpi_obj:
                    admission_hpi_obj = admission_hpi_obj[0]

                if admission_ros_obj:
                    admission_ros_obj = admission_ros_obj[0]
                    v_ros = admissionrospresentationclass_factory(admission_ros_obj)
                else:
                  v_ros = "No Review of System Recorded"

                if vital_exam_obj:
                    vital_exam_obj = vital_exam_obj[0]
                    vf = vitalexamobjpresentationclass_factory(vital_exam_obj)
                else:
                    vf = "No Vitals Recorded"

                if gen_exam_obj:
                    gen_exam_obj = gen_exam_obj[0]
                    gf = genexamobjpresentationclass_factory(gen_exam_obj)
                else:
                    gf = "No General Examination Recorded"

                if sys_exam_obj:
                    sys_exam_obj = sys_exam_obj[0]
                    sf = sysexamobjpresentationclass_factory(sys_exam_obj)
                else:
                    sf = "No Systemic Examination Recorded"

                if neuro_exam_obj:
                    neuro_exam_obj = neuro_exam_obj[0]
                    nf = neuroexamobjpresentationclass_factory(neuro_exam_obj)
                else:
                    nf = "No Neurological Examination Recorded"

                if vasc_exam_obj:
                    vasc_f = vascexamobjpresentationclass_querysetfactory(vasc_exam_obj)
                else:
                    vasc_f = "No Vascular Examination Recorded"

                d = OrderedDict()
                d['complaint']= admission_complaint_obj
                d['hpi']= admission_hpi_obj
                d['ros']= v_ros
                d['vitals']= vf
                d['gen_exam']=gf
                d['sys_exam']=sf
                d['neuro_exam']=nf
                d['vasc_exam']=vasc_f
                dict_to_append[admission] = d
                admission_obj_list.append(dict_to_append)
                #print "Vascular Exam is: "
                #print vasc_f
        else:
            error_message = "No Admissions Recorded"
        variable = RequestContext(
            request, {'user': user,
                      'admission_detail_obj': admission_detail_obj,
                      'admission_obj_list': admission_obj_list,
                      'patient_detail_obj': patient_detail_obj,
                      'error_ message': error_message
                      })
        return render_to_response('admission_detail/summary.html', variable)
    else:
        raise Http404(" Error ! Unsupported Request..")



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