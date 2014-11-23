################################################################################
# Project     : AuShadha
# Description : Generic Queries for models 
#               A dump for useful functions used everywhere
# Author      : Dr. Easwar T.R
# Date        : 19-09-2013
# License     : GNU-GPL Version 3, See AuShadha/License.txt
################################################################################

"""
 These are Queries that have been left here. 
 They are old code that needs to be moved into the respective app/queries.py module.
"""

#import json

#from AuShadha.apps.ui.ui import ui as UI

#PatientDetail = UI.get_module("PatientRegistration")
#AdmissionDetail = UI.get_module("Admission")
#VisitDetail = UI.get_module("OPD_Visit")
#VisitComplaint = UI.get_module("OPD_Visit_Complaint")
#Contact = UI.get_module("Contact")
#Phone = UI.get_module("Phone")
#Guardian = UI.get_module("Guardian")

def has_active_admission(patient):
    
    """Queries whether a given patient has an active admission."""

    from patient.models import PatientDetail
    from admission.admission.models import AdmissionDetail

    patient_id = patient.id

    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
    except(TypeError, ValueError, PatientDetail.DoesNotExist):
        return False
    adm_obj = AdmissionDetail.objects.filter(
        patient_detail=pat_obj).filter(admission_closed=False)
    if adm_obj:
        return True
    else:
        return False

def adm_for_pat(patient):
    
    """
      Returns the number of admissions for a patient after calling
      has_active_admission.

      If no admission it returns the None. Useful for Templates
      manipulation.
    """

    from patient.models import PatientDetail
    from admission.admission.models import AdmissionDetail

    patient_id = patient.id

    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
    except(TypeError, ValueError, PatientDetail.DoesNotExist):
        return False

    if has_active_admission(patient) == '0':
        return None
    else:
        all_adm_obj = AdmissionDetail.objects.filter(patient_detail=pat_obj)
        return all_adm_obj

def has_active_visit(patient):
    
    """
      Queries whether a given patient has a active visit.
      Returns Boolean. 
      Returns False in case of error.
    """

    from patient.models import PatientDetail
    from visit.visit.models import VisitDetail

    patient_id = patient.id
    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
    except(TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
        return False
    visit_obj = VisitDetail.objects.filter(
        patient_detail=pat_obj, is_active=True)
    if visit_obj:
        return True
    else:
        return False


def can_add_new_visit(patient):

    """
      Queries whether a given patient Can add a new visit.
      Takes a patient instance as a argument.
      Basically checks whether he/she has an active admission.

      If the visit adding model is changed and new visit addition is not
          permitted if an active visit is there that logic can also go here

      Returns Boolean
    """

    from patient.models import PatientDetail
#    from admission.admission.models import AdmissionDetail
    from visit.visit.models import VisitDetail
    from visit.visit_complaints.models import VisitComplaint

    patient_id = patient.id

    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)

    except(TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
        return False

    # if not has_active_visit(patient):

    #if not has_active_admission(patient):
        #return True
    #else:
        #return False
    # else:
        # return False
    return True

def visit_for_pat(patient):
    
    """
      Details the visit details for each patient.
      This is useful for display on the Patient List table in
        template. 
      Can just call this method and format a table with
        results for a quick view. 
      Can use the return value of "VisitObject" 
        to call the is_visit_active method if needed
    """

    #from patient.models import PatientDetail
    #from admission.models import AdmissionDetail
    #from visit.models import VisitDetail, VisitComplaint

    patient_id = patient.id
    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
    except (TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
        return False
    visit_obj = VisitDetail.objects.filter(patient_detail=pat_obj)
    if not visit_obj:
        return None
    else:
        return visit_obj


def get_patient_complaints(patient):

    from patient.models import PatientDetail
    from admission.admission.models import AdmissionDetail
    from visit.visit.models import VisitDetail
    from visit.visit_complaints.models import VisitComplaint

    p_id = patient.id

    try:
        pat_obj = PatientDetail.objects.get(pk=p_id)
    except(TypeError, AttributeError, NameError):
        raise Exception("Invalid ID. Raised Error")
    except(PatientDetail.DoesNotExist):
        raise Exception("Invalid Patient. No Such Patient on record")
    visit_obj = VisitDetail.objects.filter(
        patient_detail=pat_obj).order_by('-visit_date')
    visit_complaint_list = []
    if visit_obj:
        for visit in visit_obj:
            visit_complaints = VisitComplaint.objects.filter(
                visit_detail=visit)
            if visit_complaints:
                for complaint in visit_complaints:
                    dict_to_append = {}
                    dict_to_append['complaint'] = complaint.complaint
                    dict_to_append['duration'] = complaint.duration
                    dict_to_append[
                        'visit_date'] = complaint.visit_detail.visit_date.date().isoformat()
                    dict_to_append[
                        'is_active'] = complaint.visit_detail.is_active
                    dict_to_append['visit_detail'] = complaint.visit_detail
                    dict_to_append[
                        'visit_fu'] = complaint.visit_detail.has_fu_visits()
                    visit_complaint_list.append(dict_to_append)
    #jsondata = json.dumps(visit_complaint_list)
    #return json
    return visit_complaint_list




def has_contact(patient):
    """Returns a Boolean whether a particular patient has a contact or not
    in Database."""

    from patient.models import PatientDetail
    from demographics.contact.models import Contact

    patient_id = patient.id

    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
    except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
        return False
    contact = Contact.objects.filter(patient_detail=pat_obj)
    if contact:
        return contact
    else:
        return False

def has_phone(patient):
    """Returns a Boolean whether a particular patient has a contact or not
    in Database."""

    from patient.models import PatientDetail
    from demographics.phone.models import Phone

    patient_id = patient.id

    try:
        pat_obj = Phone.objects.get(pk=patient_id)
    except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
        return False
    phone = Phone.objects.filter(patient_detail=pat_obj)
    if phone:
        return phone
    else:
        return False

def has_guardian(patient):

    """Returns a Boolean whether a particular patient has a contact or not
    in Database."""

    from patient.models import PatientDetail
    from demographics.guardian.models import Guardian

    patient_id = patient.id

    try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
    except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
        return False
    guardian = Guardian.objects.filter(patient_detail=pat_obj)
    if guardian:
        return guardian
    else:
        return False
