################################################################################
# Project      : AuShadha
# Description  : Models for AuShadha OPD Visits.
# Author       : Dr. Easwar TR 
# Date         : 17-09-2013
# LICENSE      : GNU-GPL Version 3, Please see AuShadha/LICENSE.txt
################################################################################

# General Imports
from datetime import datetime, date, time
import importlib


# Django Specific Imports
from django.db import models
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput

# Application model imports
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm
from AuShadha.apps.clinic.models import Clinic, Staff

from registry.inv_and_imaging.models import ImagingInvestigationRegistry, LabInvestigationRegistry
#from patient.models import PatientDetail
#from admission.models import AdmissionDetail

PatientDetail = UI.get_module("PatientRegistration")
#AdmissionDetail = UI.get_module("Admission")
VisitComplaint = UI.get_module('OPD_Visit_Complaint')

from dijit_fields_constants import VISIT_DETAIL_FORM_CONSTANTS

DEFAULT_VISIT_DETAIL_FORM_EXCLUDES = ('patient_detail',)


CONSULT_NATURE_CHOICES = (
    ('initial', 'Initial'),
    ('fu', 'Follow-Up'),
    ('emer', 'Emergency'),
)


CONSULT_BOOKING_CATEGORY_CHOICES = (
    ('appointment', "Appointment"),
    ('telephonic', 'Telephonic / Web'),
    ('na', 'Walk-in / Emergency'),    
    ('referral', 'Referral'),
    ('starred', 'Starred'),        
)


CONSULT_REASON_CHOICES = (
    ('opd_consult', "OPD Consult"),
    ('inv_review',"Investigations Review"),
    ('emergency',"Emergency"),
    ('pre_op',"Pre-op Counselling"),
    ('post_op',"Post-op Counselling"),
    ('dressing',"Dressing"),
    ('minor_opd_procedures',"Minor OPD Procedures"),    
    ('prescription_top_up',"Prescription Top Up"),
    ('admission',"Admission"),
    ('others',"Others"),
)

CONSULT_STATUS_CHOICES = (
    ('waiting', 'Waiting'),
    ('examining', 'Examining'),
    ('review_awaited', 'Review Awaited'),
    ('admission', 'Admission'),
    ('discharged', 'Discharged'),
    ('no_show', 'No Show'),
)






class VisitDetail(AuShadhaBaseModel):

    def __init__(self, *args, **kwargs):
      super(VisitDetail,self).__init__(*args, **kwargs)
      self.__model_label__ = "visit"
      self._parent_model = 'patient_detail'
      self._can_add_list_or_json = ['visit_complaint',
                                    'visit_follow_up',
                                    'visit_ros',
                                    'visit_hpi',
                                    'visit_phyexam',
                                    'vitals',
                                    'gen',
                                    'sys',
                                    'neuro',
                                    'vasc',
                                    'visit_assessment_and_plan',
                                    'visit_soap',
                                    #'past_history',
                                    #'visit_inv',
                                    #'visit_imaging',
                                    #'visit_procedures',
                                    #'discharge'
                                    ]

      self._extra_url_actions = ['close','change_nature']

    patient_detail = models.ForeignKey(PatientDetail)
    visit_date = models.DateTimeField(auto_now=False, default=datetime.now())
    op_surgeon = models.ForeignKey(Staff)

    referring_doctor = models.CharField(max_length=30, 
                                        default="Self"
                                        )                          # Should be an FK to referring doctors model / Contacts

    consult_nature = models.CharField(max_length=30, 
                                      choices=CONSULT_NATURE_CHOICES
                                      )                            # Should be an FK to appointment model
    
    booking_category = models.CharField(max_length=30, 
                                        choices=CONSULT_BOOKING_CATEGORY_CHOICES
                                        )                          # Should ideally be an FK to appointment model
    
    consult_reason = models.CharField(max_length=30, 
                                      choices=CONSULT_REASON_CHOICES
                                      )                            # Should be an FK to appointment model
    
    status = models.CharField(max_length=30, 
                              choices=CONSULT_STATUS_CHOICES
                              )                                    # Should update via FK the appointment model

    is_active = models.BooleanField(default=True, editable=False)

    remarks = models.TextField(max_length=200,
                               default="NAD",
                               help_text="limit to 200 words"
                               )

    class Meta:
        verbose_name = "Visit Details"
        verbose_name_plural = "Visit Details"

    def __unicode__(self):
        return '%s(%s): %s: %s' % (self.patient_detail,
                                   self.id, 
                                   self.visit_date, 
                                   self.op_surgeon
                                   )

    def get_absolute_url(self):
        return '/AuShadha/visit/detail/%d/' % (self.id)

    def get_all_patient_complaints_url(self):
        return '/AuShadha/visit_complaints/complaint/get/%s/' %(self.id)

    def import_active_complaints_url(self):
        return '/AuShadha/visit_complaints/complaint/import_active_complaints/%s/' %(self.id)

    def get_all_visit_hpi_url(self):
        return '/AuShadha/visit_hpi/hpi/get_all_visit_hpi/%s/' %(self.id)

    def get_all_visit_ros_url(self):
        return '/AuShadha/visit_ros/ros/get_all_visit_ros/%s/' %(self.id)

    def get_edit_pane_header_url(self):
        return '/AuShadha/visit/get/visit_detail/edit_pane_header/%s/' %(self.id)

    def get_visit_detail_close_url(self):
        if self.is_active:
            return '/AuShadha/visit/visit/detail/close/%d/' % (self.id)
        else:
            raise Exception("Visit is already not active. Cannot Close")

    def get_visit_detail_visit_follow_up_add_url(self):
        # if self.patient_detail.has_active_visit():
            # return self.patient_detail.get_patient_visit_add_url()
        # else:
            # return False
        return '/AuShadha/visit/follow_up/add/?visit_id=%s' % (self.id)

    
    def get_visit_phyexam_add_vitals_url(self):
        return '/AuShadha/visit_phyexam/vitals/add/%s/' %(self.id)
    
    def get_visit_phyexam_add_gen_url(self):
        return '/AuShadha/visit_phyexam/gen/add/%s/' %(self.id)
    
    def get_visit_phyexam_add_sys_url(self):
        return '/AuShadha/visit_phyexam/sys/add/%s/' %(self.id)
    
    def get_visit_phyexam_add_neuro_url(self):
        return '/AuShadha/visit_phyexam/neuro/add/%s/' %(self.id)
    
    def get_visit_phyexam_add_vasc_url(self):
        return '/AuShadha/visit_phyexam/vasc/add/%s/' %(self.id)


    def has_fu_visits(self):
        id = self.id
        try:
            visit_obj = VisitDetail.objects.get(pk=id)
            fu = VisitFollowUp.objects.filter(visit_detail=visit_obj).order_by('-visit_date')
            if fu:
                return fu
            else:
                return None
        except(VisitDetail.DoesNotExist):
            raise Exception("Not Visit Detail with ID:", str(id))

    def visit_nature(self):
        return unicode(self.consult_nature)

    def visit_nature_change(self, nature):
        try:
            self.consult_nature = unicode(nature)
        except (TypeError, NameError, ValueError):
            print "ERROR:: Invalid CONSULT_NATURE_CHOICE supplied.."
            return False
        if consult_nature in ['initial', 'fu','emer']:
            self.save()
            return unicode(self.consult_nature)
        else:
            print "ERROR:: Invalid Consult Nature Change Requested.."
            return False

    def visit_status(self):
        return unicode(self.status)

    def visit_status_change(self, status):
        try:
            self.status = unicode(status)
        except (TypeError, NameError, ValueError):
            print "ERROR:: Invalid CONSULT_STATUS_CHOICES supplied.."
            return False
        if status in ['discharged', 'admission', 'review_awaited']:
            if self.status == 'discharged' or \
               self.status == 'admission':
                self._close_visit()
            else:
                self.is_active = True
                self.save()
            return unicode(self.status)
        else:
            print "ERROR:: Invalid Consult Status Change Requested.."
            return False

    def _close_visit(self):
        #id = self.id
        #visit_obj      = VisitDetail.objects.get(pk = id)
        #visit_followup = VisitFollowUp.objects.filter(visit_detail = visit_obj)
        # if visit_followup:
            # for fu in visit_followup:
                #fu.status = 'discharged'
                # fu.save()
        print "Trying to Close a visit with ID"
        print self.id
        self.is_active = False
        kwargs = {'dont_check_status': "yes"}
        self.save(**kwargs)

    def _close_all_active_visits(self):
        pat_obj = self.patient_detail
        visit_obj = VisitDetail.objects.filter(
            patient_detail=pat_obj).filter(is_active=True)
        if visit_obj:
            for visit in visit_obj:
                visit._close_visit()
            return True
        else:
            return False

    def save(self, *args, **kwargs):

        # if self.op_surgeon.clinic_staff_role == 'doctor':
        consult_nature = self.consult_nature
        print "Calling save method with args"
        print "kwargs dont_check_status is set to: ", kwargs.get('dont_check_status')

        if self.pk is not None:
            if kwargs.get('dont_check_status') is 'yes':
                kwargs = kwargs.pop('dont_check_status')
                self.status = 'discharged'
                self.is_active = False
                print "Closing the visit and saving the changes"
            else:
                if self.status == 'no_show' or self.status == 'discharged' or self.status == 'admission':
                    self.is_active = False
            super(VisitDetail, self).save(force_update=True)

        else:
            # if not self.patient_detail.has_active_visit():
                #self.consult_nature = 'initial'
            self.is_active = True
            super(VisitDetail, self).save(*args, **kwargs)

        # else:
            #raise Exception("User is not a Provider. Only Doctors can save Visits. ")

    def get_visit_complaints(self):

        import json
        v_id = self.id

        try:
            visit_obj = VisitDetail.objects.get(pk=v_id)
            pat_obj = visit_obj.patient_detail
        
        except(TypeError, AttributeError, NameError):
            raise Exception("Invalid ID. Raised Error")
        
        except(VisitDetail.DoesNotExist):
            raise Exception("Invalid Visit. No Such Visit recorded")

        #visit_fu            = VisitFollowUp.objects.filter(visit_detail = visit_obj)
        visit_complaints = VisitComplaint.objects.filter(visit_detail=visit_obj)
        visit_complaint_list = []

        if visit_complaints:

            for complaint in visit_complaints:
                dict_to_append = {}
                dict_to_append['complaint'] = complaint.complaint
                dict_to_append['duration'] = complaint.duration
                dict_to_append['visit_date'] = complaint.visit_detail.visit_date.date().isoformat()
                dict_to_append['visit_active'] = complaint.visit_detail.is_active
                visit_complaint_list.append(dict_to_append)

        #jsondata = json.dumps(visit_complaint_list)
        # return json
        return visit_complaint_list


    def has_previous_visits(self):

      try:
        visit_id = self.id

      except AttributeError:
        raise Exception("Invalid Visit Id: Null")

      visit_detail_obj = VisitDetail.objects.get(pk = int(visit_id) )
      patient_detail_obj = visit_detail_obj.patient_detail
      all_visits = VisitDetail.objects.get(patient_detail = patient_detail_obj).order_by('visit_date')

      for v in all_visits:
        if (v.visit_date <= visit_detail_obj.visit_date) and (v != visit_detail_obj):
          return True
        else:
          continue




class VisitDetailForm(AuShadhaBaseModelForm):
    

    def __init__(self, *args, **kwargs):
        self.__form_name__ = "Visit Detail Form"

        op_surgeon = ModelChoiceField(queryset=Staff.objects.filter(clinic_staff_role='doctor'))

        self.dijit_fields = VISIT_DETAIL_FORM_CONSTANTS

    class Meta:
        model = VisitDetail
        exclude = DEFAULT_VISIT_DETAIL_FORM_EXCLUDES
