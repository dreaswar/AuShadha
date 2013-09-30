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
#import ho.pisa                      as pisa
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from collections import OrderedDict

# Application Specific Model Imports-----------------------
from AuShadha.utilities.forms import AuModelFormErrorFormatter, aumodelformerrorformatter_factory

from AuShadha.apps.aushadha_users.models import AuShadhaUser
from AuShadha.apps.clinic.models import Clinic, Staff
from visit.models import *
from patient.models import PatientDetail
from admission.models import AdmissionDetail
#from physician.models import PhysicianDetail
from demographics.models import Contact, Guardian, Phone, Demographics
from medication_list.models import MedicationList
from allergy_list.models import Allergy
from social_history.models import SocialHistory
from family_history.models import FamilyHistory
from medical_history.models import MedicalHistory
from surgical_history.models import SurgicalHistory
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


# Module Vars:
complaint_add_icon_template = get_template(
    'visit_template_snippets/icons/complaints_add.html')
complaint_remove_icon_template = get_template(
    'visit_template_snippets/icons/complaints_remove.html')

generic_table_form_add_icon_template = get_template(
    'visit_template_snippets/icons/generic_add_icon.html')
generic_table_form_remove_icon_template = get_template(
    'visit_template_snippets/icons/generic_remove_icon.html')


# views start here;;
@login_required
def visit_list(request):
    if request.user:
        user = request.user
        if request.method == "GET":
            visit_obj = VisitDetail.objects.all().order_by('visit_date')
            variable = RequestContext(request, {'user': user,
                                                'visit_obj': visit_obj,
                                                })
            return render_to_response('visit_detail/visit_list.html', variable)
        else:
            raise Http404("Bad Request:: " + str(request.method) + " ")
    else:
        return HttpResponseRedirect('/AuShadha/login/')


@login_required
def visit_home(request, id='id'):
    pass

#

@login_required
def visit_json(request, patient_id = None):
    try:
        action = unicode(request.GET.get('action'))
        if patient_id:
          patient_id = int(patient_id)
        else:
          patient_id = int(request.GET.get('patient_id'))          
        if action == 'add':
            return patient_visit_add(request, patient_id)
        patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")
    patient_visit_obj = VisitDetail.objects.filter(
        patient_detail=patient_detail_obj)
    data = []
    if patient_visit_obj:
        for visit in patient_visit_obj:
            i = 0
            data_to_append = {}
            data_to_append['id'] = visit.id
            data_to_append[
                'visit_date'] = visit.visit_date.date().isoformat() + i
            data_to_append['op_surgeon'] = visit.op_surgeon.__unicode__()
            data_to_append['is_active'] = visit.is_active
            data_to_append['referring_doctor'] = visit.referring_doctor
            data_to_append['consult_nature'] = visit.consult_nature
            data_to_append['remarks'] = visit.remarks
            data_to_append['edit'] = visit.get_edit_url()
            data_to_append['del'] = visit.get_del_url()
            data.append(data_to_append)
            i += 1
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")



@login_required
def render_visit_tree(request, patient_id=None):
    if request.method == "GET" and request.is_ajax():
        if patient_id:
            patient_id = int(patient_id)
        else:
            try:
                patient_id = int(request.GET.get('patient_id'))
                pat_obj = PatientDetail.objects.get(pk=patient_id)
            except(AttributeError, NameError, KeyError, TypeError, ValueError):
                raise Http404("ERROR! Bad Request Parameters")
            except(AttributeError, NameError, KeyError, TypeError, ValueError):
                raise Http404("ERROR! Requested Patient Data Does not exist")

            pat_obj.generate_urls()
            pat_urls = pat_obj.urls

            adm_obj = AdmissionDetail.objects.filter(
                patient_detail=pat_obj)
            visit_obj = VisitDetail.objects.filter(
                patient_detail=pat_obj)


            prev_visit_obj = VisitDetail.objects.filter(
                patient_detail=pat_obj).filter(is_active=False)
            active_visit_obj = VisitDetail.objects.filter(
                patient_detail=pat_obj).filter(is_active=True)

            demographics_obj = Demographics.objects.filter(
                patient_detail=pat_obj)
            social_history_obj = SocialHistory.objects.filter(
                patient_detail=pat_obj)
            family_history_obj = FamilyHistory.objects.filter(
                patient_detail=pat_obj)
            medical_history_obj = MedicalHistory.objects.filter(
                patient_detail=pat_obj)
            surgical_history_obj = SurgicalHistory.objects.filter(
                patient_detail=pat_obj)

            medication_list_obj = MedicationList.objects.filter(
                patient_detail=pat_obj)
            allergy_obj = Allergy.objects.filter(
                patient_detail=pat_obj)

            pat_inv_obj = VisitInv.objects.filter(
                visit_detail__patient_detail=pat_obj)
            pat_imaging_obj = VisitImaging.objects.filter(
                visit_detail__patient_detail=pat_obj)

            data = {
                "identifier": "id",
                "label": "name",
                "items": [
                              {"name": "Procedures", "type": "application", "id": "PROC",
                               "len": 1,
                               "addUrl": None,
                               },

                              {"name": "History", "type": "application", "id": "HISTORY",
                               "len": 1,
                               "addUrl": None,
                               },

                              {"name": "Medication", "type": "application", "id": "MEDICATION_LIST",
                               "len": 1,
                               "addUrl": None,
                               },

                              {"name": "Investigation", "type": "application", "id": "INV",
                               "len": 1,
                               "addUrl": None,
                               },

                              {"name": "Imaging", "type": "application", "id": "IMAG",
                               "len": 1,
                               "addUrl": None,
                               },

                              #{"name"  : "Media" , "type":"application", "id":"MEDIA" ,
                              #"len"   : 1,
                              #"addUrl": None,
                              #'children':[
                    #{"name"  : "Documents" , "type":"patient_documents_module", "id":"DOCS" ,
                    #"len"   : 1,
                    #"addUrl": None,
                    #},
                    #{"name"  : "Images" , "type":"patient_images_module", "id":"IMAGES" ,
                    #"len"   : 1,
                    #"addUrl": None,
                    #}
                    #]
                              #}
                ]
            }

            tree_item_list = data['items']

            if pat_obj.can_add_new_visit():
                dict_to_append = {"name": "New OPD Visit",
                                  "type": "application",
                                  "id": "NEW_OPD_VISIT",
                                  "len": len(visit_obj),
                                  "addUrl": pat_urls['add']['visit']
                                  }
                tree_item_list.insert(0, dict_to_append)

            if active_visit_obj:
                active_visits = VisitDetail.objects.filter(
                    patient_detail=pat_obj).filter(is_active=True)
                active_visits_base_dict = {"name": "Active Visits",
                                           "type": "application",
                                           "id": "ACTIVE_VISITS",
                                           "len": True,
                                           "addUrl": None,
                                           'editUrl': None,
                                           'delUrl': None,
                                           'children': []
                                           }
                for active_visit in active_visits:
                    active_visit.generate_urls()
                    av_urls = active_visit.urls
                    base_dict = {
                        "name": active_visit.visit_date.date().isoformat(),
                        "type": "active_visit",
                        "id": "ACTIVE_VISITS_" + str(active_visit.id),
                        "len": True,
                        "addUrl": None,
                        'editUrl': av_urls['edit'],
                        'delUrl': av_urls['del'],
                        'children': [
                            {"name": "Add Follow-Up",
                                "type": "visit_follow_up_add",
                                "id": "VISIT_FOLLOW_UP_ADD_" + str(active_visit.id),
                                "len": 1,
                                "addUrl": av_urls['add']['follow_up'],
                             },

                            {"name": "Orders",
                                     "type": "application",
                                     "id": "ACTIVE_VISIT_" + str(active_visit.id) + "_ORDERS_AND_PRESCRIPTION",
                                     "len": 1,
                                     "addUrl": None,
                             },

                            {"name": "Close",
                                "type": "close_visit",
                                "id": "VISIT_CLOSE_" + str(active_visit.id),
                                "len": 1,
                                "addUrl": active_visit.get_visit_detail_close_url(),
                             },

                            #{"name"      : "Edit" ,
                            #"type"       : "visit",
                            #"id"         : "ACTIVE_VISIT_" + str(active_visit.id) ,
                            #"len"        : 1,
                            #"addUrl"     : None,
                            #"absoluteUrl": active_visit.get_absolute_url(),
                            #"editUrl"    : active_visit.get_edit_url(),
                            #"deUrl"      : active_visit.get_del_url()
                            #},

                            #{"name"  : "Diagnosis" , "type":"application", "id":"DIAG" ,
                            #"len"   : 1,
                            #"addUrl": None,
                            #},

                            #{"name"  : "Advice" , "type":"advice","id":"ADVICE" ,
                            #"len"   : 1,
                            #"addUrl": None,
                            #},

                            #{"name"  : "Procedure" , "type":"procedure", "id":"PROC" ,
                            #"len"   : 1,
                            #"addUrl": None,
                            #},

                            #{"name"  : "Calendar" , "type":"application", "id":"CAL" ,
                            #"len"   : 1,
                            #"addUrl": None,
                            #},
                        ]
                    }
                    active_visits_base_dict['children'].append(base_dict)

                    if active_visit.has_fu_visits():
                        fu_visit = active_visit.has_fu_visits()
                        fu_base_dict = {"name": "Follow-ups",
                                        "type": "fu_visits",
                                        "id": "",
                                        "len": 1,
                                        "addUrl": None,
                                        "absoluteUrl": None,
                                        "children": []
                                        }
                        fu_sub_dict = {
                            "name": "", "type": "visit", "id": "", "editUrl": "", "delUrl": ""}
                        base_dict['children'].append(fu_base_dict)

                        for fu in fu_visit:
                            fu_dict_to_append = fu_sub_dict.copy()

                            fu_dict_to_append = {
                                "name": fu.visit_date.date().isoformat(),
                                "type": "fu_visit",
                                "id": "FU_VISIT_" + str(fu.id),
                                "editUrl": fu.get_edit_url(),
                                "delUrl": fu.get_del_url(),
                                "children": [{"name": "Orders",
                                              "type": "application",
                                              "id": "FU_VISIT_" + str(fu.id) + "_ORDERS_AND_PRESCRIPTION",
                                              "len": 1,
                                              "addUrl": None,
                                              }]
                            }
                            fu_base_dict['children'].append(fu_dict_to_append)

                tree_item_list.insert(1, active_visits_base_dict)
                #tree_item_list.insert(1, base_dict)

            if prev_visit_obj:
                base_dict = {"name": "Closed Visits", "type":
                             "application", "id": "CLOSED_VISITS", 'children': []}
                sub_dict = {
                    "name": "", "type": "visit", "id": "", "editUrl": "", "delUrl": ""}
                for visit in prev_visit_obj:
                    visit.generate_urls()
                    v_urls = visit.urls
                    dict_to_append = sub_dict.copy()
                    dict_to_append['name'] = visit.visit_date.date(
                    ).isoformat() + "(" + visit.op_surgeon.__unicode__() + ")"
                    dict_to_append[
                        'id'] = "CLOSED_VISIT_" + unicode(visit.id)
                    dict_to_append['absoluteUrl'] = visit.get_absolute_url()
                    dict_to_append['editUrl'] = v_urls['edit']
                    dict_to_append['delUrl'] = v_urls['del']
                    dict_to_append['children'] = [{"name": "Orders",
                                                   "type": "application",
                                                   "id": "CLOSED_VISIT_" + str(visit.id) + "_ORDERS_AND_PRESCRIPTION",
                                                   "len": 1,
                                                   "addUrl": None,
                                                   }]
                    base_dict['children'].append(dict_to_append)
                    if visit.has_fu_visits():
                        fu_visit = visit.has_fu_visits()
                        fu_base_dict = {"name": "Follow-ups",
                                        "type": "fu_visits",
                                        "id": "CLOSED_FOLLOW_UP_VISITS_" + str(visit.id),
                                        "len": 1,
                                        "addUrl": None,
                                        "absoluteUrl": None,
                                        "children": []
                                        }
                        fu_sub_dict = {
                            "name": "", "type": "visit", "id": "", "editUrl": "", "delUrl": ""}
                        dict_to_append['children'].append(fu_base_dict)

                        for fu in fu_visit:
                            fu_dict_to_append = fu_sub_dict.copy()
                            fu_dict_to_append = {
                                "name": fu.visit_date.date().isoformat(),
                                "type": "fu_visit",
                                "id": "CLOSED_FU_VISIT_" + str(fu.id),
                                "editUrl": fu.get_edit_url(),
                                "delUrl": fu.get_del_url(),
                                "children": [{"name": "Orders",
                                              "type": "application",
                                              "id": "CLOSED_FU_VISIT_" + str(fu.id) + "_ORDERS_AND_PRESCRIPTION",
                                              "len": 1,
                                              "addUrl": None,
                                              }]
                            }
                            fu_base_dict['children'].append(fu_dict_to_append)

                tree_item_list.insert(2, base_dict)

            # if visit_obj:
                #data['items'][1]['children'] = []
                #children_list  = data['items'][1]['children']
                # for visit in visit_obj:
                    #dict_to_append = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
                    #dict_to_append['name']    = visit.visit_date.date().isoformat() + "("+ visit.op_surgeon.__unicode__() +")"
                    #dict_to_append['id']      = "VISIT_"+ unicode(visit.id)
                    #dict_to_append['absoluteUrl'] = visit.get_absolute_url()
                    #dict_to_append['editUrl']     = visit.get_edit_url()
                    #dict_to_append['delUrl']      = visit.get_del_url()
                    # children_list.append(dict_to_append)
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type="application/json")
    else:
        raise Http404("Bad Request")


@login_required
def render_visit_list(request):
    """View for Generating Visit List Takes on Request Object as argument."""
    user = request.user
    keys = [
        "sort( date_of_visit)", "sort(-date_of_visit)", "sort(+date_of_visit)",
        "sort( op_surgeon)", "sort(-op_surgeon)", "sort(+op_surgeon)",
    ]
    key_sort_map = {
        "sort(+date_of_visit)": "visit_date",
        "sort( date_of_visit)": "visit_date",
        "sort(-date_of_visit)": "-visit_date",
        "sort(+op_surgeon)": "op_surgeon",
        "sort( op_surgeon)": "op_surgeon",
        "sort(-op_surgeon)": "-op_surgeon",
    }
    for key in request.GET:
        if key in keys:
            sort = key_sort_map[key]
            all_visits = VisitDetail.objects.all().order_by(sort)
        else:
            all_visits = VisitDetail.objects.all().order_by('-visit_date')
    data = []
    for visit in all_visits:
        data_to_append = {}
        data_to_append['id'] = visit.id
        data_to_append['date_of_visit'] = visit.visit_date.strftime(
            "%d/%m/%Y %H:%M:%S")
        data_to_append['surgeon'] = visit.op_surgeon.__unicode__()
        data_to_append[
            'patient_hospital_id'] = visit.patient_detail.patient_hospital_id
        data_to_append['patient'] = visit.patient_detail.__unicode__()
        data_to_append['age'] = visit.patient_detail.age
        data_to_append['sex'] = visit.patient_detail.sex
        data_to_append['active'] = visit.is_active
        data_to_append['del'] = visit.get_edit_url()
        data_to_append['edit'] = visit.get_del_url()
        data.append(data_to_append)
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")

#


def get_visit_related_obj_urls(request, id=None):
    """Receives request and generates URLS for adding/editing a particular
    VisitDetail and its related Objects (VisitComplaint, VisitHPI, VisitROS).

    If a VisitDetail has no corresponding related object it returns its addUrl else
    its editUrl. If like in case of VisitComplaint object it returns a list,
    the aggregated URL is sent as List.

    if a VisitDetail itsels DoesNotExist, it returns a success=False in JSON.

    This is needed for other chained AJAX requests to populate HTML into
    DIV tags in visit/base_add.html or visit/base_edit.html templates
    This return a JSON for the use of calling an AJAX

    """

    print "Returning URL for Visit Related Objected with Visit ID of : " + str(id)
    user = request.user
    success = False
    error_message = "No Visits Recorded"
    data = {'visitDetailUrl': '',
            'visitComplaintUrl': '',
            'visitHPIUrl': '',
            'visitROSUrl': ''
            }
    if request.method == "GET" and request.is_ajax():
        try:
            id = int(id)
            visit_detail_obj = VisitDetail.objects.get(pk=id)
            visit_complaint_obj = VisitComplaint.objects.filter(
                visit_detail=visit_detail_obj)
            visit_hpi_obj = VisitHPI.objects.filter(
                visit_detail=visit_detail_obj)
            visit_ros_obj = VisitROS.objects.filter(
                visit_detail=visit_detail_obj)
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
            json = simplejson.dumps(data)
            return render_to_response('application/json', json)

        json = simplejson.dumps(data)
        return render_to_response('application/json', json)

    else:
        raise Http404(" Error ! Unsupported Request..")


def visit_add(request, id=None):
    """Receives request to Add VisitDetail, VisitComplaints, VisitHPI, VisitROS
    and Physical Examination and routes it."""
    pass


def visit_edit(request, id=None):
    """Receives request to Edit VisitDetail, VisitComplaints, VisitHPI,
    VisitROS and Physical Examination and routes it."""
    pass


def visit_del(request, id=None):
    """Receives request to Edit VisitDetail, VisitComplaints, VisitHPI,
    VisitROS and Physical Examination and routes it."""
    pass

#


@login_required
def visit_detail_list(request, patient_id = None):
    user = request.user
    if request.method == "GET" and request.is_ajax():
        try:
            if patient_id:
              patient_id = int(patient_id)
            else:
              patient_id = int(request.GET.get('patient_id'))
            patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
            visit_detail_obj = VisitDetail.objects.filter(
                patient_detail=patient_detail_obj).order_by('-visit_date')
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (PatientDetail.DoesNotExist):
            raise Http404("Requested Patient Does not exist.")
        visit_form_list = []
        if visit_detail_obj:
            error_message = None
            for visit in visit_detail_obj:
#        visit_list = []
                visit_form_list.append(
                    [VisitDetailForm(instance=visit), visit])
#        visit_form_list.append(visit_list)
        else:
            error_message = "No Visits Recorded"
        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_form_list': visit_form_list,
                      'patient_detail_obj': patient_detail_obj,
                      'error_message': error_message
                      })
        return render_to_response('visit_detail/list.html', variable)
    else:
        raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_summary(request, patient_id = None):

    user = request.user

    if request.method == "GET" and request.is_ajax():
        try:
            if patient_id:
              patient_id = int(patient_id)
            else:
              patient_id = int(request.GET.get('patient_id') )
            print "Listing Summary for patient with ID: " + str(patient_id)
            patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
            visit_detail_obj = VisitDetail.objects.filter(
                patient_detail=patient_detail_obj).order_by('-visit_date')
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (PatientDetail.DoesNotExist):
            raise Http404("Requested Patient Does not exist.")

        visit_obj_list = []
        if visit_detail_obj:
            error_message = "Listing the Visits in ", visit_detail_obj
            print "Listing the Visits in ", visit_detail_obj
            for visit in visit_detail_obj:
                dict_to_append = OrderedDict()
                dict_to_append[visit] = None
                print "Aggregating sub-modules in visit: ", visit
                visit_complaint_obj = VisitComplaint.objects.filter(
                    visit_detail=visit)
                visit_hpi_obj = VisitHPI.objects.filter(
                    visit_detail=visit)
                visit_ros_obj = VisitROS.objects.filter(
                    visit_detail=visit)
                vital_exam_obj = VitalExam_FreeModel.objects.filter(
                    visit_detail=visit)
                gen_exam_obj = GenExam_FreeModel.objects.filter(
                    visit_detail=visit)
                sys_exam_obj = SysExam_FreeModel.objects.filter(
                    visit_detail=visit)
                neuro_exam_obj = PeriNeuroExam_FreeModel.objects.filter(
                    visit_detail=visit)
                vasc_exam_obj = VascExam_FreeModel.objects.filter(
                    visit_detail=visit)

                if visit_hpi_obj:
                    visit_hpi_obj = visit_hpi_obj[0]

                if visit_ros_obj:
                    visit_ros_obj = visit_ros_obj[0]
                    v_ros = visitrospresentationclass_factory(visit_ros_obj)
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
                d['complaint']= visit_complaint_obj
                d['hpi']= visit_hpi_obj
                d['ros']= v_ros
                d['vitals']= vf
                d['gen_exam']=gf
                d['sys_exam']=sf
                d['neuro_exam']=nf
                d['vasc_exam']=vasc_f
                dict_to_append[visit] = d
                visit_obj_list.append(dict_to_append)
        else:
            error_message = "No Visits Recorded"
        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_obj_list': visit_obj_list,
                      'patient_detail_obj': patient_detail_obj,
                      'error_message': error_message
                      })
        return render_to_response('visit_detail/summary.html', variable)
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_add(request, patient_id = None, nature='initial'):
    """ Adds a new VisitDetail Object and related Objects: VisitComplaint,VisitROS, VisitHPI
        Takes request and id of PatientDetail object
        the nature of visit is defaulted to 'initial'.
        Implementation of separate visits for 'initial' , 'fu' etc.. can be implemented later.
    """
    print "Received request to add VisitDetail"

    user = request.user
    success = False
    error_message = None
    form_errors = []

    try:
        if patient_id:
          patient_id = int(patient_id)
        else:
          patient_id = int(request.GET.get('patient_id'))
        patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
        #print "Patient is: ", patient_detail_obj
        visit_detail_objs = VisitDetail.objects.filter(
            patient_detail=patient_detail_obj).filter(is_active=True)

        visit_complaint_formset_prefix="visit_complaints"
        vasc_exam_formset_prefix = "vasc_exam"
        initial_data = [{'location':"Dorsalis Pedis",'side':'right','character':'normal'}]
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")
    except (PatientDetail.DoesNotExist):
        raise Http404("Requested Patient Does not exist.")

    if not patient_detail_obj.can_add_new_visit():
        error_message = '''Cannot add new visit now.
                        There may be a active admission / visit. 
                        Please close that and try again
                    '''
        raise Http404(error_message)

    else:
        print patient_detail_obj, " can add VisitDetail"
        visit_detail_obj = VisitDetail(patient_detail=patient_detail_obj)

        visit_complaint_obj = VisitComplaint(visit_detail=visit_detail_obj)
        visit_hpi_obj = VisitHPI(visit_detail=visit_detail_obj)
        visit_ros_obj = VisitROS(visit_detail=visit_detail_obj)

        vital_exam_free_model_obj = VitalExam_FreeModel(
            visit_detail=visit_detail_obj)
        gen_exam_free_model_obj = GenExam_FreeModel(
            visit_detail=visit_detail_obj)
        sys_exam_free_model_obj = SysExam_FreeModel(
            visit_detail=visit_detail_obj)
        neuro_exam_free_model_obj = PeriNeuroExam_FreeModel(
            visit_detail=visit_detail_obj)
        vasc_exam_free_model_obj = VascExam_FreeModel(
            visit_detail=visit_detail_obj)

        generic_add_icon_html = generic_table_form_add_icon_template.render(
            RequestContext(request, {'user': user}))
        generic_remove_icon_html = generic_table_form_remove_icon_template.render(
            RequestContext(request, {'user': user}))

        VascExam_FreeModelFormset = modelformset_factory(VascExam_FreeModel,
                                              form=VascExam_FreeModelForm,
                                              can_delete=True,
                                              can_order=True,
                                              extra=1
                                              )

        VisitComplaintFormset = modelformset_factory(VisitComplaint,
                                                     form=VisitComplaintAddForm,
                                                     can_delete=True,
                                                     can_order=True,
                                                     )
        complaint_add_icon_html = complaint_add_icon_template.render(
            RequestContext(request, {'user': user}))
        complaint_remove_icon_html = complaint_remove_icon_template.render(
            RequestContext(request, {'user': user}))

        complaint_form_var_dict = {'prefix': visit_complaint_formset_prefix,
                                   'total_form_id': visit_complaint_formset_prefix+"-TOTAL_FORMS",
                                   'form_count':''
                                   } # Ultimately this may be better way to pass the vars to template

        complaint_form_auto_id = "id_"+ visit_complaint_formset_prefix + \
          "_new_complaint_" + str(id)
        complaint_total_form_auto_id = "id_"+visit_complaint_formset_prefix + \
          "-TOTAL_FORMS_new_complaint_" + str(id)
        vasc_exam_form_auto_id = "id_"+vasc_exam_formset_prefix + \
          "_new_vasc_exam_free_model_" + str(id)
        vasc_total_form_auto_id = "id_"+ vasc_exam_formset_prefix + \
          "-TOTAL_FORMS_new_vasc_exam_free_model_" + str(id)

        if request.method == "GET" and request.is_ajax():

            if nature == 'initial':
                print "Adding an Initial Visit for ", patient_detail_obj
                visit_detail_form = VisitDetailForm(
                    initial={
                        'visit_date': datetime.datetime.now().date().isoformat(),
                        'consult_nature': 'initial',
                        'status': 'examining',
                        'op_surgeon': user
                    },
                    instance=visit_detail_obj,
                    auto_id="id_new_visit_detail" + str(id) + "_%s")

                #complaint_formset_auto_id = "id_%s"+"_add_visit_complaint_"+ str(id)
                #complaint_total_form_auto_id = "id_form-TOTAL_FORMS_add_visit_complaint_"+str(id)

                # visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj,
                                                          # auto_id  =
                                                          # "id_new_visit_complaint"+
                                                          # str(id)+"_%s")
                visit_complaint_formset = VisitComplaintFormset(
                    queryset=VisitComplaint.objects.none(),
                    auto_id=complaint_form_auto_id,
                    prefix=visit_complaint_formset_prefix)
                #visit_complaint_form_html = visit_complaint_add(request,id=id)
                visit_hpi_form = VisitHPIForm(instance=visit_hpi_obj,
                                              auto_id="id_new_visit_hpi" + str(id) + "_%s")
                visit_ros_form = VisitROSForm(instance=visit_ros_obj,
                                              auto_id="id_new_visit_ros" + str(id) + "_%s")

                vital_exam_free_model_form = VitalExam_FreeModelForm(
                    instance=vital_exam_free_model_obj,
                    auto_id="id_new_vital_exam_free_model" + str(id) + "_%s")
                gen_exam_free_model_form = GenExam_FreeModelForm(
                    instance=gen_exam_free_model_obj,
                    auto_id="id_new_gen_exam_free_model" + str(id) + "_%s")
                sys_exam_free_model_form = SysExam_FreeModelForm(
                    instance=sys_exam_free_model_obj,
                    auto_id="id_new_sys_exam_free_model" + str(id) + "_%s")
                neuro_exam_free_model_form = PeriNeuroExam_FreeModelForm(
                    instance=neuro_exam_free_model_obj,
                    auto_id="id_new_neuro_exam_free_model" + str(id) + "_%s")
                #vasc_exam_free_model_form = VascExam_FreeModelForm(
                    #instance=vasc_exam_free_model_obj,
                    #auto_id=vasc_exam_form_auto_id)

                vasc_exam_free_model_formset = VascExam_FreeModelFormset(
                    queryset=VascExam_FreeModel.objects.none(),
                    auto_id=vasc_exam_form_auto_id,
                    initial=initial_data,
                    prefix=vasc_exam_formset_prefix)

                variable = RequestContext(
                    request, {
                        'user': user,
                        'visit_detail_obj': visit_detail_obj,
                        'visit_detail_form': visit_detail_form,
                        'visit_complaint_formset': visit_complaint_formset,
                        #'visit_complaint_form_html'   : visit_complaint_form_html,
                        'visit_hpi_form': visit_hpi_form,
                        'visit_ros_form': visit_ros_form,

                        'vital_exam_free_model_form': vital_exam_free_model_form,
                        'gen_exam_free_model_form': gen_exam_free_model_form,
                        'sys_exam_free_model_form': sys_exam_free_model_form,
                        'neuro_exam_free_model_form': neuro_exam_free_model_form,
                        #'vasc_exam_free_model_form': vasc_exam_free_model_form,
                        'vasc_exam_free_model_formset' :vasc_exam_free_model_formset,
                        'vasc_exam_form_auto_id':vasc_exam_form_auto_id,
                        'vasc_total_form_auto_id': vasc_exam_formset_prefix+"-TOTAL_FORMS",

                        'patient_detail_obj': patient_detail_obj,
                        'error_message': error_message,
                        'complaint_add_icon_html': complaint_add_icon_html,
                        'complaint_remove_icon_html': complaint_remove_icon_html,
                        'generic_add_icon_html':generic_add_icon_html,
                        'generic_remove_icon_html':generic_remove_icon_html,

                        'success': success,
                        'complaint_form_auto_id': complaint_form_auto_id,
                        'complaint_total_form_auto_id': visit_complaint_formset_prefix+"-TOTAL_FORMS",
                        
                        'form_action':'add'

                    })
                return render_to_response('visit_detail/add.html', variable)

            elif nature == 'fu':
                # TODO
                pass

        elif request.method == "POST" and request.is_ajax():
            print "Received request to add visit..."

            visit_detail_form = VisitDetailForm(
                request.POST, instance=visit_detail_obj)
            #visit_complaint_form = VisitComplaintForm(request.POST, instance = visit_complaint_obj)
            #VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)
            visit_complaint_formset = VisitComplaintFormset(
                request.POST, auto_id=complaint_form_auto_id,
                prefix=visit_complaint_formset_prefix)
            visit_hpi_form = VisitHPIForm(
                request.POST, instance=visit_hpi_obj)
            visit_ros_form = VisitROSForm(
                request.POST, instance=visit_ros_obj)

            vital_exam_free_model_form = VitalExam_FreeModelForm(
                request.POST, instance=vital_exam_free_model_obj)
            gen_exam_free_model_form = GenExam_FreeModelForm(
                request.POST, instance=gen_exam_free_model_obj)
            sys_exam_free_model_form = SysExam_FreeModelForm(
                request.POST, instance=sys_exam_free_model_obj)
            neuro_exam_free_model_form = PeriNeuroExam_FreeModelForm(
                request.POST, instance=neuro_exam_free_model_obj)
            vasc_exam_free_model_form = VascExam_FreeModelForm(
                request.POST, instance=vasc_exam_free_model_obj)
            vasc_exam_free_model_formset = VascExam_FreeModelFormset(
                request.POST, auto_id=vasc_exam_form_auto_id,
                prefix=vasc_exam_formset_prefix)

            if visit_detail_form.is_valid()         and \
                visit_complaint_formset.is_valid()    and \
                visit_hpi_form.is_valid()             and \
                visit_ros_form.is_valid()             and \
                vital_exam_free_model_form.is_valid() and \
                gen_exam_free_model_form.is_valid()   and \
                sys_exam_free_model_form.is_valid()   and \
                neuro_exam_free_model_form.is_valid() and \
                vasc_exam_free_model_formset.is_valid():

                saved_visit = visit_detail_form.save()

                saved_visit_complaints = visit_complaint_formset.save(
                    commit=False)
                #print "Saved visit is:"
                #print saved_visit
                # print saved_visit_complaints
                for complaint in saved_visit_complaints:
                    #print "Saving Complaints..."
                    # print complaint
                    complaint.visit_detail = saved_visit
                    complaint.save()

                saved_visit_hpi = visit_hpi_form.save(commit=False)
                saved_visit_hpi.visit_detail = saved_visit
                saved_visit_hpi.save()

                saved_visit_ros = visit_ros_form.save(commit=False)
                saved_visit_ros.visit_detail = saved_visit
                saved_visit_ros.save()

                saved_vital_exam = vital_exam_free_model_form.save(
                    commit=False)
                saved_vital_exam.visit_detail = saved_visit
                saved_vital_exam.physician = saved_visit.op_surgeon
                saved_vital_exam.save()

                saved_gen_exam = gen_exam_free_model_form.save(commit=False)
                saved_gen_exam.visit_detail = saved_visit
                saved_gen_exam.physician = saved_visit.op_surgeon
                saved_gen_exam.save()

                saved_sys_exam = sys_exam_free_model_form.save(commit=False)
                saved_sys_exam.visit_detail = saved_visit
                saved_sys_exam.physician = saved_visit.op_surgeon
                saved_sys_exam.save()

                saved_neuro_exam = neuro_exam_free_model_form.save(
                    commit=False)
                saved_neuro_exam.visit_detail = saved_visit
                saved_neuro_exam.physician = saved_visit.op_surgeon
                saved_neuro_exam.save()

                #saved_vasc_exam = vasc_exam_free_model_form.save(
                    #commit=False)
                #saved_vasc_exam.visit_detail = saved_visit
                #saved_vasc_exam.physician = saved_visit.op_surgeon
                #saved_vasc_exam.save()

                saved_vasc_exam = vasc_exam_free_model_formset.save(
                    commit=False)
                for vasc in saved_vasc_exam:
                    #print "Saving Vascular Exam... : ", vasc
                    vasc.visit_detail = saved_visit
                    vasc.physician = saved_visit.op_surgeon
                    vasc.created_at = datetime.datetime.now()
                    vasc.modified_at = datetime.datetime.now()
                    vasc.save()
                    #print "Vascular Exam, " , vasc, " Saved"

                success = True
                error_message = "Visit Added Successfully"

            else:
                error_message = ''' <h4>Visit Could not be Saved.
                            Please check the forms for errors</h4>
                        '''
                errors = aumodelformerrorformatter_factory(visit_detail_form)     + \
                    aumodelformerrorformatter_factory(visit_ros_form)             + \
                    aumodelformerrorformatter_factory(vital_exam_free_model_form) + \
                    aumodelformerrorformatter_factory(gen_exam_free_model_form)   + \
                    aumodelformerrorformatter_factory(sys_exam_free_model_form)   + \
                    aumodelformerrorformatter_factory(neuro_exam_free_model_form) + '\n'
                    #aumodelformerrorformatter_factory(vasc_exam_free_model_form)  + '\n'

                for form in visit_complaint_formset:
                    errors += aumodelformerrorformatter_factory(form)
                for form in vasc_exam_free_model_formset:
                    errors += aumodelformerrorformatter_factory(form)

                error_message += ('\n' + errors)

            data = {'success': success,
                    'error_message': error_message
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_edit(request, visit_id = None):

    user = request.user
    error_message = None    
    VisitComplaintFormset = modelformset_factory(VisitComplaint,
                                                 form=VisitComplaintEditForm,
                                                 extra=0
                                                 )

    if request.method == "GET" and request.is_ajax():
        try:
            if visit_id:
              visit_id = int(visit_id)
            else:
              visit_id = int(request.GET.get('visit_id'))
            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)

            visit_complaint_obj = VisitComplaint.objects.filter(
                visit_detail=visit_detail_obj)
            visit_hpi_obj = VisitHPI.objects.filter(
                visit_detail=visit_detail_obj)
            visit_ros_obj = VisitROS.objects.filter(
                visit_detail=visit_detail_obj)
            vital_exam_free_model_obj = VitalExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            gen_exam_free_model_obj = GenExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            sys_exam_free_model_obj = SysExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            neuro_exam_free_model_obj = PeriNeuroExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            vasc_exam_free_model_obj = VascExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Patient Does not exist.")

        visit_complaint_formset_prefix="edit_visit_complaints_"+str(visit_id)
        vasc_exam_formset_prefix = "edit_vasc_exam_"+str(visit_id)
        form_field_auto_id = 'id_edit_visit_detail_' + str(visit_id)
        complaint_formset_auto_id = "id_"+visit_complaint_formset_prefix +\
          "_edit_visit_complaint_" + str(visit_id)
        complaint_total_form_auto_id = "id_"+visit_complaint_formset_prefix+\
          "-TOTAL_FORMS_edit_visit_complaint_" + str(visit_id)

        data = {'visit_date': visit_detail_obj.visit_date.date().isoformat()}
        visit_detail_form = VisitDetailForm(
            initial=data, instance=visit_detail_obj, auto_id=form_field_auto_id + "_%s")

        visit_complaint_formset = VisitComplaintFormset(
            queryset=VisitComplaint.objects.filter(
                visit_detail=visit_detail_obj),
            auto_id=complaint_formset_auto_id,
            prefix = visit_complaint_formset_prefix
        )
        complaint_count = len(visit_complaint_obj)
        complaint_add_icon_template = get_template(
            'visit_template_snippets/icons/complaints_add.html')
        complaint_remove_icon_template = get_template(
            'visit_template_snippets/icons/complaints_remove.html')
        complaint_add_icon_html = complaint_add_icon_template.render(
            RequestContext(request, {'user': user}))
        complaint_remove_icon_html = complaint_remove_icon_template.render(
            RequestContext(request, {'user': user}))

        # if visit_complaint_obj:
            #visit_complaint_obj = visit_complaint_obj[0]
            #c_auto_id = 'id_edit_visit_complaint_'+str(visit_complaint_obj.id)
            #visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj, auto_id = c_auto_id +"_%s")
        # else:
            #visit_complaint_form = None
            #visit_complaint_formset  = None
        if visit_hpi_obj:
            visit_hpi_obj = visit_hpi_obj[0]
            h_auto_id = 'id_edit_visit_hpi_' + str(visit_hpi_obj.id)
            visit_hpi_form = VisitHPIForm(
                instance=visit_hpi_obj, auto_id=h_auto_id + "_%s")
        else:
            visit_hpi_form = None

        if visit_ros_obj:
            visit_ros_obj = visit_ros_obj[0]
            r_auto_id = 'id_edit_visit_ros_' + str(visit_ros_obj.id)
            visit_ros_form = VisitROSForm(
                instance=visit_ros_obj, auto_id=r_auto_id + "_%s")
        else:
            visit_ros_form = None

        if vital_exam_free_model_obj:
            vital_exam_free_model_obj = vital_exam_free_model_obj[0]
            vital_auto_id     = 'id_edit_vital_exam_free_model_' + \
                str(vital_exam_free_model_obj.id)
            vital_exam_free_model_form = VitalExam_FreeModelForm(
                instance=vital_exam_free_model_obj,
                auto_id=vital_auto_id + "_%s")
        else:
            vital_auto_id     = 'id_add_vital_exam_free_model_' + \
                str(visit_detail_obj.id)
            vital_exam_free_model_form = VitalExam_FreeModelForm(
                instance=VitalExam_FreeModel(
                    visit_detail=visit_detail_obj),
                auto_id=vital_auto_id + "_%s")

        if gen_exam_free_model_obj:
            gen_exam_free_model_obj = gen_exam_free_model_obj[0]
            gen_auto_id     = 'id_edit_gen_exam_free_model_' + \
                str(gen_exam_free_model_obj.id)
            gen_exam_free_model_form = GenExam_FreeModelForm(
                instance=gen_exam_free_model_obj,
                auto_id=gen_auto_id + "_%s")
        else:
            gen_auto_id     = 'id_add_gen_exam_free_model_' + \
                str(visit_detail_obj.id)
            gen_exam_free_model_form = GenExam_FreeModelForm(
                instance=GenExam_FreeModel(visit_detail=visit_detail_obj),
                auto_id=gen_auto_id + "_%s")

        if sys_exam_free_model_obj:
            sys_exam_free_model_obj = sys_exam_free_model_obj[0]
            sys_auto_id     = 'id_edit_sys_exam_free_model_' + \
                str(sys_exam_free_model_obj.id)
            sys_exam_free_model_form = SysExam_FreeModelForm(
                instance=sys_exam_free_model_obj,
                auto_id=sys_auto_id + "_%s")
        else:
            sys_auto_id     = 'id_add_sys_exam_free_model_' + \
                str(visit_detail_obj.id)
            sys_exam_free_model_form = SysExam_FreeModelForm(
                instance=SysExam_FreeModel(visit_detail=visit_detail_obj),
                auto_id=sys_auto_id + "_%s")

        if neuro_exam_free_model_obj:
            neuro_exam_free_model_obj = neuro_exam_free_model_obj[0]
            neuro_auto_id     = 'id_edit_neuro_exam_free_model_' + \
                str(neuro_exam_free_model_obj.id)
            neuro_exam_free_model_form = PeriNeuroExam_FreeModelForm(
                instance=neuro_exam_free_model_obj,
                auto_id=neuro_auto_id + "_%s")
        else:
            neuro_auto_id     = 'id_add_neuro_exam_free_model_' + \
                str(visit_detail_obj.id)
            neuro_exam_free_model_form = PeriNeuroExam_FreeModelForm(
                instance=PeriNeuroExam_FreeModel(
                    visit_detail=visit_detail_obj),
                auto_id=neuro_auto_id + "_%s")

        if vasc_exam_free_model_obj:
            #vasc_exam_free_model_obj = vasc_exam_free_model_obj[0]
            vasc_exam_form_auto_id = "id_"+vasc_exam_formset_prefix  + \
              "_edit_vasc_exam_free_model_" + str(id)
            vasc_total_form_auto_id = "id_"+vasc_exam_formset_prefix + \
              "-TOTAL_FORMS_edit_vasc_exam_free_model_" + str(id)
            VascExam_FreeModelFormset = modelformset_factory(VascExam_FreeModel,
                                                      form=VascExam_FreeModelForm,
                                                      extra=0
                                                      )

            #vasc_auto_id     = 'id_edit_vasc_exam_free_model_' + \
                #str(vasc_exam_free_model_obj.id)
            #vasc_exam_free_model_form = VascExam_FreeModelForm(
                #instance=vasc_exam_free_model_obj,
                #auto_id=vasc_exam_form_auto_id)

        else:
            vasc_exam_form_auto_id = "id_"+vasc_exam_formset_prefix + \
              "_add_vasc_exam_free_model_" + str(id)
            vasc_total_form_auto_id = "id_"+ vasc_exam_formset_prefix +\
              "-TOTAL_FORMS_add_vasc_exam_free_model_" + str(id)
            vasc_exam_formset_prefix = "add_vasc_exam_"+str(id)
            VascExam_FreeModelFormset = modelformset_factory(VascExam_FreeModel,
                                                      form=VascExam_FreeModelForm,
                                                      extra=1
                                                      )

            #vasc_auto_id     = 'id_add_vasc_exam_free_model_' + \
                #str(visit_detail_obj.id)
            #vasc_exam_free_model_form = VascExam_FreeModelForm(
                #instance=VascExam_FreeModel(visit_detail=visit_detail_obj),
                #auto_id=vasc_exam_form_auto_id)
        vasc_exam_free_model_formset = VascExam_FreeModelFormset(
                queryset=VascExam_FreeModel.objects.filter(visit_detail = visit_detail_obj),
                auto_id=vasc_exam_form_auto_id,
                prefix=vasc_exam_formset_prefix
                )
        generic_add_icon_html = generic_table_form_add_icon_template.render(
            RequestContext(request, {'user': user}))
        generic_remove_icon_html = generic_table_form_remove_icon_template.render(
            RequestContext(request, {'user': user}))

        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_detail_form': visit_detail_form,
                      #'visit_complaint_form'  : visit_complaint_form  ,
                      'visit_complaint_formset': visit_complaint_formset,
                      'visit_hpi_form': visit_hpi_form,
                      'visit_ros_form': visit_ros_form,

                      'vital_exam_free_model_form': vital_exam_free_model_form,
                      'gen_exam_free_model_form': gen_exam_free_model_form,
                      'sys_exam_free_model_form': sys_exam_free_model_form,
                      'neuro_exam_free_model_form': neuro_exam_free_model_form,
                      #'vasc_exam_free_model_form': vasc_exam_free_model_form,
                      'vasc_exam_free_model_formset': vasc_exam_free_model_formset,
                      'vasc_exam_form_auto_id':vasc_exam_form_auto_id,
                      'vasc_total_form_auto_id':vasc_exam_formset_prefix+"-TOTAL_FORMS",

                      'patient_detail_obj': visit_detail_obj.patient_detail,
                      'error_message': error_message,
                      'complaint_count': complaint_count,
                      'complaint_add_icon_html': complaint_add_icon_html,
                      'complaint_remove_icon_html': complaint_remove_icon_html,
                      'complaint_formset_auto_id': complaint_formset_auto_id,
                      'complaint_total_form_auto_id': visit_complaint_formset_prefix+"-TOTAL_FORMS",
                      'generic_add_icon_html':generic_add_icon_html,
                      'generic_remove_icon_html':generic_remove_icon_html,
                      
                      'form_action':'edit'
                      })
        return render_to_response('visit_detail/edit.html', variable)

    if request.method == "POST" and request.is_ajax():
        try:
            if visit_id:
              visit_id = int(visit_id)
            else:
              visit_id = request.POST.get('visit_id')
            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)

            visit_complaint_formset_prefix="edit_visit_complaints_"+str(visit_id)
            vasc_exam_formset_prefix = "edit_vasc_exam_"+str(visit_id)

            visit_complaint_obj = VisitComplaint.objects.filter(
                visit_detail=visit_detail_obj)
            visit_hpi_obj = VisitHPI.objects.filter(
                visit_detail=visit_detail_obj)
            visit_ros_obj = VisitROS.objects.filter(
                visit_detail=visit_detail_obj)

            vital_exam_free_model_obj = VitalExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            gen_exam_free_model_obj = GenExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            sys_exam_free_model_obj = SysExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            neuro_exam_free_model_obj = PeriNeuroExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)
            vasc_exam_free_model_obj = VascExam_FreeModel.objects.filter(
                visit_detail=visit_detail_obj)

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")
        success = False
        error_message = None
        VascExam_FreeModelFormset = modelformset_factory(VascExam_FreeModel,
                                                  form=VascExam_FreeModelForm
                                                  )
        if visit_complaint_obj and visit_hpi_obj and visit_ros_obj:
            visit_detail_form = VisitDetailForm(
                request.POST, instance=visit_detail_obj)
            #visit_complaint_form   = VisitComplaintForm(request.POST, instance = visit_complaint_obj[0])
            complaint_formset_auto_id = "id_"+visit_complaint_formset_prefix + \
                "_edit_visit_complaint_" + str(id)
            complaint_total_form_auto_id = "id_"+ visit_complaint_formset_prefix+\
              "-TOTAL_FORMS_edit_visit_complaint_" + str(id)
            #VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)
            visit_complaint_formset = VisitComplaintFormset(
                request.POST, queryset=visit_complaint_obj,
                prefix=visit_complaint_formset_prefix,
                auto_id=complaint_formset_auto_id)

            visit_hpi_form = VisitHPIForm(
                request.POST, instance=visit_hpi_obj[0])
            visit_ros_form = VisitROSForm(
                request.POST, instance=visit_ros_obj[0])

            if vital_exam_free_model_obj:
                vital_exam_free_model_form = VitalExam_FreeModelForm(
                    request.POST, instance=vital_exam_free_model_obj[0])
            else:
                vital_exam_free_model_obj = VitalExam_FreeModel(
                    visit_detail=visit_detail_obj)
                vital_exam_free_model_form = VitalExam_FreeModelForm(
                    request.POST, instance=vital_exam_free_model_obj)

            if gen_exam_free_model_obj:
                gen_exam_free_model_form = GenExam_FreeModelForm(
                    request.POST, instance=gen_exam_free_model_obj[0])
            else:
                gen_exam_free_model_obj = GenExam_FreeModel(
                    visit_detail=visit_detail_obj)
                gen_exam_free_model_form = GenExam_FreeModelForm(
                    request.POST, instance=gen_exam_free_model_obj)

            if sys_exam_free_model_obj:
                sys_exam_free_model_form = SysExam_FreeModelForm(
                    request.POST, instance=sys_exam_free_model_obj[0])
            else:
                sys_exam_free_model_obj = SysExam_FreeModel(
                    visit_detail=visit_detail_obj)
                sys_exam_free_model_form = SysExam_FreeModelForm(
                    request.POST, instance=sys_exam_free_model_obj)

            if neuro_exam_free_model_obj:
                neuro_exam_free_model_form = PeriNeuroExam_FreeModelForm(
                    request.POST, instance=neuro_exam_free_model_obj[0])
            else:
                neuro_exam_free_model_obj = PeriNeuroExam_FreeModel(
                    visit_detail=visit_detail_obj)
                neuro_exam_free_model_form = PeriNeuroExam_FreeModelForm(
                    request.POST, instance=neuro_exam_free_model_obj)

            if vasc_exam_free_model_obj:
                #vasc_exam_free_model_form = VascExam_FreeModelForm(
                    #request.POST, instance=vasc_exam_free_model_obj[0])
                vasc_exam_formset_auto_id = "id_"+vasc_exam_formset_prefix + \
                "_edit_vasc_exam_" + str(id)
                vasc_exam_total_form_auto_id = "id_"+ vasc_exam_formset_prefix+\
                "-TOTAL_FORMS_edit_vasc_exam_" + str(id)
                vasc_exam_free_model_formset = VascExam_FreeModelFormset(
                    request.POST, queryset=vasc_exam_free_model_obj,
                    prefix=vasc_exam_formset_prefix,
                    auto_id=vasc_exam_formset_auto_id)

            else:
                #vasc_exam_free_model_obj = VascExam_FreeModel(
                    #visit_detail=visit_detail_obj)
                vasc_exam_formset_auto_id = "id_"+vasc_exam_formset_prefix + \
                "_add_vasc_exam_" + str(id)
                vasc_exam_total_form_auto_id = "id_"+ vasc_exam_formset_prefix+\
                "-TOTAL_FORMS_add_vasc_exam_" + str(id)
                vasc_exam_free_model_formset = VascExam_FreeModelFormset(
                    request.POST, 
                    queryset=VascExam_FreeModel.objects.filter(visit_detail=visit_detail_obj),
                    prefix=vasc_exam_formset_prefix,
                    auto_id=vasc_exam_formset_auto_id)

                #vasc_exam_free_model_form = VascExam_FreeModelForm(
                    #request.POST, instance=vasc_exam_free_model_obj)

            if visit_detail_form.is_valid()         and \
                visit_complaint_formset.is_valid()    and \
                visit_hpi_form.is_valid()             and \
                visit_ros_form.is_valid()             and \
                vital_exam_free_model_form.is_valid() and \
                gen_exam_free_model_form.is_valid()   and \
                sys_exam_free_model_form.is_valid()   and \
                neuro_exam_free_model_form.is_valid() and \
                vasc_exam_free_model_formset.is_valid():                
                #vasc_exam_free_model_form.is_valid()


                saved_visit = visit_detail_form.save()

                saved_visit_complaints = visit_complaint_formset.save(
                    commit=False)
                #print "Saved visit is:"
                #print saved_visit
                # print saved_visit_complaints
                for complaint in saved_visit_complaints:
                    #print "Saving Complaints..."
                    # print complaint
                    complaint.visit_detail = saved_visit
                    complaint.save()

                saved_visit_hpi = visit_hpi_form.save(commit=False)
                saved_visit_hpi.visit_detail = saved_visit
                saved_visit_hpi.save()

                saved_visit_ros = visit_ros_form.save(commit=False)
                saved_visit_ros.visit_detail = saved_visit
                saved_visit_ros.save()

                saved_vital_exam = vital_exam_free_model_form.save(
                    commit=False)
                saved_vital_exam.visit_detail = saved_visit
                saved_vital_exam.physician = saved_visit.op_surgeon
                saved_vital_exam.save()

                saved_gen_exam = gen_exam_free_model_form.save(commit=False)
                saved_gen_exam.visit_detail = saved_visit
                saved_gen_exam.physician = saved_visit.op_surgeon
                saved_gen_exam.save()

                saved_sys_exam = sys_exam_free_model_form.save(commit=False)
                saved_sys_exam.visit_detail = saved_visit
                saved_sys_exam.physician = saved_visit.op_surgeon
                saved_sys_exam.save()

                saved_neuro_exam = neuro_exam_free_model_form.save(
                    commit=False)
                saved_neuro_exam.visit_detail = saved_visit
                saved_neuro_exam.physician = saved_visit.op_surgeon
                saved_neuro_exam.save()

                #saved_vasc_exam = vasc_exam_free_model_form.save(
                    #commit=False)
                #saved_vasc_exam.visit_detail = saved_visit
                #saved_vasc_exam.physician = saved_visit.op_surgeon
                #saved_vasc_exam.save()

                saved_vasc_exam = vasc_exam_free_model_formset.save(
                    commit=False)
                #print saved_vasc_exam
                for vasc in saved_vasc_exam:
                    #print "Saving ", vasc
                    vasc.visit_detail = saved_visit
                    vasc.physician = saved_visit.op_surgeon
                    vasc.modified_at = datetime.datetime.now()
                    vasc.save()
                    #print "Vascular Exam saved"

                success = True
                error_message = "Visit Edited Successfully"
            else:
                success = False
                error_message = ''' <h4>Visit Could not be Saved.
                            Please check the forms for errors</h4>
                        '''

                errors = aumodelformerrorformatter_factory(visit_detail_form)     + \
                    aumodelformerrorformatter_factory(visit_ros_form)             + \
                    aumodelformerrorformatter_factory(vital_exam_free_model_form) + \
                    aumodelformerrorformatter_factory(gen_exam_free_model_form)   + \
                    aumodelformerrorformatter_factory(sys_exam_free_model_form)   + \
                    aumodelformerrorformatter_factory(neuro_exam_free_model_form) + '\n'
                    #aumodelformerrorformatter_factory(vasc_exam_free_model_form)  + '\n'
                for form in visit_complaint_formset:
                    errors += aumodelformerrorformatter_factory(form)
                for form in vasc_exam_free_model_formset:
                    errors += aumodelformerrorformatter_factory(form)
                error_message += ('\n' + errors)
            data = {'success': success,
                    'error_message': error_message
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404(
                "ERROR!  The visit has not associated complaints, HPI or ROS to edit")
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_del(request, visit_id = None):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        if user.has_perm('visit.delete_visitdetail'):
            try:
                if visit_id:
                  visit_id = int(visit_id)
                else:
                  visit_id = int(request.GET.get('visit_id'))
                visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            except (TypeError, NameError, ValueError, AttributeError, KeyError):
                raise Http404("Error ! Invalid Request Parameters. ")
            except (VisitDetail.DoesNotExist):
                raise Http404("Requested Patient Does not exist.")
            error_message = None
            visit_detail_obj.delete()
            success = True
            error_message = "Successfully Deleted Visit."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            success = False
            error_message = "Insufficient Permission. Could not delete."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_close(request, visit_id = None):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        if user.has_perm('visit.change_visitdetail'):
            try:
                if visit_id :
                  visit_id= int(visit_id)
                else:
                  visit_id = int(request.GET.get('visit_id'))
                visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            except (TypeError, NameError, ValueError, AttributeError, KeyError):
                raise Http404("Error ! Invalid Request Parameters. ")
            except (VisitDetail.DoesNotExist):
                raise Http404("Requested Visit Does not exist.")
            # visit_detail_obj._close_all_active_visits()
            visit_detail_obj._close_visit()
            error_message = None
            success = True
            error_message = "Successfully Closed Visit."
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            success = False
            error_message = "Insufficient Permissions to Change Visit"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")





@login_required
def visit_follow_up_add(request, visit_id = None):

    user = request.user
    print "Received Request to add a follow up visit from ", user
    if request.method == "GET" and request.is_ajax():
        try:
            if visit_id:
              visit_id = int(visit_id)
            else:
              visit_id = int(request.GET.get('visit_id'))
            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")
        except(visit_detail_obj.is_active == False):
            raise Http404("The Visit is Closed. Cannot add Followup Visits")

        visit_follow_up_obj = VisitFollowUp(visit_detail=visit_detail_obj)
        visit_follow_up_form = VisitFollowUpForm(
            instance=visit_follow_up_obj,
            auto_id='id_visit_follow_up_' +
            str(visit_detail_obj.id) +
            "_%s"
        )
        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_follow_up_obj': visit_follow_up_obj,
                      'visit_follow_up_form': visit_follow_up_form,
                      'patient_detail_obj': visit_detail_obj.patient_detail
                      })
        return render_to_response('visit_follow_up/add.html', variable)

    if request.method == "POST" and request.is_ajax():
        print "Received request to add a Follow-Up OPD Visit..."
        try:
            if visit_id : 
              visit_id = int(visit_id)
            else:
              visit_id = int(request.GET.get('visit_id'))
            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")

        visit_follow_up_obj = VisitFollowUp(visit_detail=visit_detail_obj)
        visit_follow_up_form = VisitFollowUpForm(
            request.POST, instance=visit_follow_up_obj)

        if visit_follow_up_form.is_valid():
            saved_follow_up = visit_follow_up_form.save()
            success = True
            error_message = "Follow Up Visit Added Successfully"
        else:
            success = False
            error_message = "Error! Follow-up visit Could not be added"
        data = {'success': success,
                'error_message': error_message
                }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_follow_up_edit(request, follow_up_id = None):

    user = request.user
    print "Received Request to add a follow up visit from ", user
    if request.method == "GET" and request.is_ajax():
        try:
            if follow_up_id: 
              follow_up_id= int(follow_up_id)
            else:
              follow_up_id = int(request.GET.get('follow_up_id'))
            visit_follow_up_obj = VisitFollowUp.objects.get(pk=follow_up_id)
            visit_detail_obj = visit_follow_up_obj.visit_detail
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitFollowUp.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")
        except(visit_follow_up_obj.visit_detail.is_active == False):
            raise Http404("The Visit is Closed. Cannot add Followup Visits")

        visit_follow_up_form = VisitFollowUpForm(
            instance=visit_follow_up_obj,
            auto_id='id_visit_follow_up_' +
            str(visit_follow_up_obj.id) +
            "_%s"
        )
        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_follow_up_obj': visit_follow_up_obj,
                      'visit_follow_up_form': visit_follow_up_form,
                      'patient_detail_obj': visit_detail_obj.patient_detail
                      })
        return render_to_response('visit_follow_up/edit.html', variable)

    if request.method == "POST" and request.is_ajax():
        print "Received request to add a Follow-Up OPD Visit..."
        try:
            if follow_up_id: 
              follow_up_id= int(follow_up_id)
            else:
              follow_up_id = int(request.POST.get('follow_up_id'))
            visit_follow_up_obj = VisitFollowUp.objects.get(pk=follow_up_id)
            visit_detail_obj = visit_follow_up_obj.visit_detail
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitFollowUp.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")
        except(visit_follow_up_obj.visit_detail.is_active == False):
            raise Http404("The Visit is Closed. Cannot add Followup Visits")

        visit_follow_up_form = VisitFollowUpForm(
            request.POST, instance=visit_follow_up_obj)

        if visit_follow_up_form.is_valid():
            saved_follow_up = visit_follow_up_form.save()
            success = True
            error_message = "Follow Up Visit Edited Successfully"
        else:
            success = False
            error_message = "Error! Follow-up visit Could not be added"
        data = {'success': success,
                'error_message': error_message
                }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_follow_up_del(request, follow_up_id = None):

    if request.method == "GET" and request.is_ajax():
        user = request.user
        if user.has_perm('visit.delete_visitfollowup'):
            try:
                if follow_up_id:
                  follow_up_id = int(follow_up_id)
                else:
                  follow_up_id = int(request.GET.get('follow_up_id'))
                visit_follow_up_obj = VisitFollowUp.objects.get(pk=follow_up_id)
            except (TypeError, NameError, ValueError, AttributeError, KeyError):
                raise Http404("Error ! Invalid Request Parameters. ")
            except (VisitFollowUp.DoesNotExist):
                raise Http404("Requested Patient Does not exist.")
            error_message = None
            visit_follow_up_obj.delete()
            success = True
            error_message = "Successfully Deleted Visit."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            success = False
            error_message = "Insufficient Permission. Could not delete."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")


#

@login_required
def visit_complaint_add(request, visit_id=None):
    user = request.user
    success = False
    error_message = "Complaint Added Successfully"
    form_errors = []
    try:
        if visit_id :
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))
        visit_detail_obj = VisitDetail.objects.get(pk= visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail
        visit_complaint_objs = VisitComplaint.objects.filter(
            visit_detail=visit_detail_obj)
        visit_complaint_obj = VisitComplaint(visit_detail=visit_detail_obj)
        VisitComplaintFormset = modelformset_factory(
            VisitComplaint, form=VisitComplaintForm, extra=1)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")

    if request.method == "GET" and request.is_ajax():
        print "Received GET request to add Visit Complaints "
    # visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj,
                                                  # auto_id  =
                                                  # "id_new_visit_complaint"+
                                                  # str(id)+"_%s")
        visit_complaint_formset = VisitComplaintFormset(
            queryset=visit_complaint_objs)
        #print visit_complaint_formset
        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_complaint_formset': visit_complaint_formset,
                      'patient_detail_obj': patient_detail_obj
                      })
        return render_to_response('visit_complaints/add.html', variable)

    if request.method == "POST" and request.is_ajax():
        print "Received POST request to add Visit complaints ..."
        #visit_complaint_form = VisitComplaintForm(request.POST, instance = visit_complaint_obj)
        visit_complaint_formset = VisitComplaintFormset(request.POST)

        if visit_complaint_formset.is_valid():
            saved_visit_complaint = visit_complaint_formset.save(commit=False)
            for complaint in saved_visit_complaint:
                complaint.visit_detail = saved_visit
                complaint.save()

            success = True
        else:
            success = False
            error_message = '''Error! Complaint Could not be added.
                          Please check the forms for errors
                      '''
        data = {'success': success,
                'error_message': error_message
                }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_complaint_edit(request, complaint_id=None):
    pass


@login_required
def visit_complaint_del(request, complaint_id=None):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        if user.has_perm('visit.delete_visitcomplaint'):
            try:
                if complaint_id : 
                  complaint_id = int(complaint_id)
                else:
                  complaint_id = int(request.GET.get('complaint_id'))
                visit_complaint_obj = VisitComplaint.objects.get(pk=complaint_id)
            except (TypeError, NameError, ValueError, AttributeError, KeyError):
                raise Http404("Error ! Invalid Request Parameters. ")
            except (VisitComplaint.DoesNotExist):
                raise Http404("Requested Complaint Does not exist.")
            error_message = None
            visit_complaint_obj.delete()
            success = True
            error_message = "Successfully Deleted Visit Complaint"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            success = False
            error_message = "Insufficient Permission. Could not delete."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")






####################################### PDF Render #############################

# Will be removed
# Better to rely on plain HTML
# This is lot of work and not an absolute necessity
# Add more complexity, external dependency to the project
# Cumbersome to style it with current tools
# Creates a significant additional skillset to learn with a very limited use case 

@login_required
def render_visit_pdf(request, id):
    if request.user:
        user = request.user
        try:
            id = int(id)
            visit_detail_obj = VisitDetail.objects.get(pk=id)
        except(ValueError, AttributeError, TypeError, VisitDetail.DoesNotExist):
            raise Http404(
                'Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
        pat_detail_obj = visit_detail_obj.patient_detail
        if request.method == 'GET':
            variable = RequestContext(request,
                                      {'user': user,
                                       'pat_detail_obj': pat_detail_obj,
                                       'visit_detail_obj': visit_detail_obj,
                                       }
                                      )
            return render_to_response('visit_detail/visit_pdf_template.html', variable)
        elif request.method == 'POST':
            pass
        else:
            raise Http404("Bad Request.." + str(request.method))
    else:
        return HttpResponseRedirect('/login')


@login_required
def render_patient_visits_pdf(request, id):
    if request.user:
        user = request.user
        try:
            id = int(id)
            patient_detail_obj = PatientDetail.objects.get(pk=id)
        except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
            raise Http404(
                'Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
        visit_detail_obj = VisitDetail.objects.filter(
            patient_detail=patient_detail_obj)
        visit_obj_list = []

        if visit_detail_obj:
            error_message = "Listing the Visits"
            for visit in visit_detail_obj:
                dict_to_append = {}
                visit_complaint_obj = VisitComplaint.objects.filter(
                    visit_detail=visit)
                visit_hpi_obj = VisitHPI.objects.filter(
                    visit_detail=visit)
                visit_ros_obj = VisitROS.objects.filter(
                    visit_detail=visit)
                if visit_ros_obj:
                    visit_ros_obj = visit_ros_obj[0]
                dict_to_append[visit] = {'complaint': visit_complaint_obj,
                                         'hpi': visit_hpi_obj,
                                         'ros': format_ros(visit_ros_obj)
                                         }
                visit_obj_list.append(dict_to_append)
        else:
            error_message = "No Visits Recorded"

        if request.method == 'GET':
            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_obj_list': visit_obj_list,
                          'patient_detail_obj': patient_detail_obj,
                          'error_message': error_message,
                          'pagesize': "A4"
                          })

            template = get_template(
                'visit_detail/patient_visit_pdf_template.html')
            html = template.render(variable)
            result = StringIO.StringIO()
            pdf = pisa.pisaDocument(
                StringIO.StringIO(html.encode("UTF-8")), result)

            if not pdf.err:
                return HttpResponse(result.getvalue(), mimetype='application/pdf')
            return HttpResponse("Error Generating PDF.. %s" % (html))

        else:
            raise Http404("Bad Request.." + str(request.method))
    else:
        return HttpResponseRedirect('/login')
