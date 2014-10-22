################################################################################
# Project     : AuShadha
# Description : Utilities for Patient
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

import json
from django.core import serializers
#from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic
from AuShadha.apps.ui.ui import ui as UI


from .models import PatientDetail, PatientDetailForm
from patient.dijit_widgets.tree import PatientTree

Demographics = UI.get_module('Demographics')
Contact = UI.get_module('Contact')
Phone = UI.get_module('Phone')
Guardian = UI.get_module('Guardian')
EmailAndFax = UI.get_module('EmailAndFax')

MedicalHistory = UI.get_module('MedicalHistory')
SurgicalHistory = UI.get_module('SurgicalHistory')
SocialHistory = UI.get_module('SocialHistory')
FamilyHistory = UI.get_module('FamilyHistory')
Immunisation = UI.get_module('Immunisation')

Allergy = UI.get_module('AllergyList')
MedicationList = UI.get_module("MedicationList")

AdmissionDetail = UI.get_module("Admission")

VisitDetail = UI.get_module("OPD_Visit")
VisitImaging = UI.get_module("OPD_Visit_Imaging")
VisitInv = UI.get_module("OPD_Visit_Inv")
VisitComplaint = UI.get_module("OPD_Visit_Complaint")

################ Some Utilities #################################################

def check_before_adding(patient_obj):
    patient_object = patient_obj
    patient_id = patient_object.patient_hospital_id
    all_patients = PatientDetail.objects.all()
    active_admissions = AdmissionDetail.objects.filter(
        patient_detail=patient_object).filter(admission_closed='False')
    active_visit = patient_object.has_active_visit()
    id_list = []
    for patient in all_patients:
        id_list.append(patient.patient_hospital_id)
    if patient_id in id_list:
        error = "This ID is already Taken. Please renter and retry"
        #print error
        return False
    else:
        if active_visit == False:
            if active_admissions == False:
                print 'All checked.. Everything ok.. '
                return True
            else:
                error = 'This patient has active admissions. Please discharge and retry.'
                #print error
                return False
        else:
            error = "This patient has active visit. Please discharge and retry."
            #print error
            return False


def return_patient_json(patient,success = True):
   p = ModelInstanceJson(patient)
   return p()


def get_all_complaints(visit):

    v_id = visit.id
    pat_obj  = visit.patient_detail

    visit_obj = VisitDetail.objects.filter(patient_detail = pat_obj).order_by('-visit_date')
    visit_complaint_list = []

    if visit_obj:

        for visit in visit_obj:
            visit_complaints = VisitComplaint.objects.filter( visit_detail = visit )

            if visit_complaints:
                for complaint in visit_complaints:
                    dict_to_append = {}
                    dict_to_append['complaint'] = complaint.complaint
                    dict_to_append['duration'] = complaint.duration
                    dict_to_append['visit_date'] = complaint.visit_detail.visit_date.date().isoformat()
                    dict_to_append['is_active'] = complaint.visit_detail.is_active
                    dict_to_append['visit_detail'] = complaint.visit_detail
                    dict_to_append['visit_fu'] = complaint.visit_detail.has_fu_visits()

                    visit_complaint_list.append(dict_to_append)

    return visit_complaint_list
