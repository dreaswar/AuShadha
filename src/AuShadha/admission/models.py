################################################################################
# Project      : AuShadha
# Description  : Admission Models 
# Author       : Dr.Easwar T.R
# Date         : 18-09-2013
# Licence      : GNU GPL version3 Please see AuShadha/LICENSE.txt 
################################################################################

import datetime
from django.db import models
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.apps.clinic.models import Staff
from registry.inv_and_imaging.models import ImagingInvestigationRegistry, LabInvestigationRegistry
from patient.models import PatientDetail
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput

from dijit_fields_constants import ADMISSION_DETAIL_FORM_CONSTANTS, \
                                   ADMISSION_COMPLAINTS_FORM_CONSTANTS,\
                                   ADMISSION_HPI_FORM_CONSTANTS,\
                                   ADMISSION_IMAGING_FORM_CONSTANTS,\
                                   ADMISSION_INVESTIGATION_FORM_CONSTANTS,\
                                   ADMISSION_PAST_HISTORY_FORM_CONSTANTS,\
                                   ADMISSION_ROS_FORM_CONSTANTS

IMAGING_CHOICES = (	('MRI', 'MRI'), ('X-Ray', 'X-Ray'),
                  ('USG', 'USG'), ('CT', 'CT'), ('Others', 'Others'	))


DEFAULT_ADMISSION_DETAIL_FORM_EXCLUDES = ('patient_detail',)

class AdmissionDetail(AuShadhaBaseModel):

    """
      Model to managed the admissions for a particular patient.

    """
    def __init__(self, *args, **kwargs):
      self.__model_label__ = "admission"
      self._parent_model = 'patient_detail'
      self._can_add_list_or_json = [
                                    #'complaint',
                                    #'ros',
                                    #'hpi',
                                    #'soap',
                                    #'phy_exam',
                                    #'past_history',
                                    #'inv',
                                    #'imaging',
                                    #'procedure',
                                    #'discharge',
                                    #'diagnosis',
                                    #'discharge',
                                    #'incident',
                                    #'progress_notes',
                                    #'admission_notes',
                                    #'discharge_summary',
                                   ]
      self._extra_url_actions = ['close',]

    date_of_admission = models.DateTimeField(auto_now=False)
    room_or_ward = models.CharField(max_length=30, blank=True, null=True)
    admission_closed = models.BooleanField(editable = False)
    admitting_physician = models.ForeignKey(Staff)
    remarks = models.TextField(max_length = 1000, null = True, blank = True, default = "NAD")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now_add=False, editable=True)
    patient_detail = models.ForeignKey(PatientDetail)


    class Meta:
        verbose_name = "Admission Basic Data"
        verbose_name_plural = "Admission Basic Data"
        ordering = ('date_of_admission', 'admitting_physician', 'patient_detail')

    def __unicode__(self):
        return "%s ,Pat:%s, Phy: %s" % (self.date_of_admission, self.patient_detail, self.admitting_physician)


class AdmissionComplaint(AuShadhaBaseModel):
    
    def __init__(self, *args, **kwargs):
      self.__model_label__ = "complaint"
      self._parent_model = 'admission_detail'

    complaint = models.CharField(max_length=30, help_text='limit to 30 words')
    duration = models.CharField(max_length=30, help_text='limit to 30 words')
    admission_detail = models.ForeignKey(AdmissionDetail)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    #base_model = models.OneToOneField(AuShadhaBaseModel, parent_link=True)

    def __unicode__(self):
        return '%s : %s' % (self.complaint, self.duration)

    class Meta:
        verbose_name = "Presenting Complaint"
        verbose_name_plural = "Presenting Complaint"
        ordering = ('admission_detail', 'created_at', 'complaint')



class AdmissionHPI(AuShadhaBaseModel):
    
    def __init__(self, *args, **kwargs):
      self.__model_label__ = "hpi"
      self._parent_model = 'admission_detail'
    
    hpi = models.TextField('History of Presenting Illness', 
                           max_length=1000, 
                           help_text='limit to 1000 words')
    admission_detail = models.ForeignKey(AdmissionDetail)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s' % (self.hpi)

    class Meta:
        #unique_together   = ('hpi', 'admission_detail')
        verbose_name = "History of Presenting Illness"
        verbose_name_plural = "History of Presenting Illness"
        ordering = ('admission_detail', 'created_at', 'hpi')


class AdmissionPastHistory(AuShadhaBaseModel):

    def __init__(self, *args, **kwargs):
      self.__model_label__ = "past_history"
      self._parent_model = 'admission_detail'


    past_history = models.TextField(
        'Past History ', max_length=1000, help_text='limit to 1000 words')
    admission_detail = models.ForeignKey(AdmissionDetail)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s' % (self.past_history)

    class Meta:
        #unique_together   = ('past_history', 'admission_detail')
        verbose_name = "Past History"
        verbose_name_plural = "Past History"
        ordering = ('admission_detail', 'created_at', 'past_history')


class AdmissionImaging(AuShadhaBaseModel):

    def __init__(self, *args, **kwargs):
      self.__model_label__ = "imaging"
      self._parent_model = 'admission_detail'

    modality = models.ForeignKey(ImagingInvestigationRegistry)
    finding = models.TextField('Finding', max_length=1000, help_text='limit to 1000 words')
    admission_detail = models.ForeignKey(AdmissionDetail)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __unicode__(self):
        return '''%s: %s \n(%s)''' % (self.modality, self.finding, self.created_at.date().isoformat() )

    def __trimmed_unicode__(self):
        return '''%s: %s ... \n(%s)''' % (self.modality, self.finding[0:5], self.created_at.date().isoformat() )

    class Meta:
        verbose_name = "Imaging Studies"
        verbose_name_plural = "Imaging Studies"
        ordering = ('admission_detail', 'created_at', 'modality')


class AdmissionROS(AuShadhaBaseModel):

    def __init__(self, *args, **kwargs):
      self.__model_label__ = 'admission_ros'
      self._parent_model = 'admission_detail'

    const_symp = models.TextField(
        'Constitutional', max_length=500, default="Nil")
    eye_symp = models.TextField(
        'Eyes', max_length=500, default="Nil")
    ent_symp = models.TextField(
        'Ear, Nose, Throat', max_length=500, default="Nil")
    cvs_symp = models.TextField(
        'Cardiovascular', max_length=500, default="Nil")
    resp_symp = models.TextField(
        'Respiratory', max_length=500, default="Nil")
    gi_symp = models.TextField(
        'Gastrointestinal', max_length=500, default="Nil")
    gu_symp = models.TextField(
        'Genitourinary', max_length=500, default="Nil")
    ms_symp = models.TextField(
        'Musculoskeletal', max_length=500, default="Nil")
    integ_symp = models.TextField(
        'Integumentary/ Breast', max_length=500, default="Nil")
    neuro_symp = models.TextField(
        'Neurological', max_length=500, default="Nil")
    psych_symp = models.TextField(
        'Psychiatric', max_length=500, default="Nil")
    endocr_symp = models.TextField(
        'Endocrine', max_length=500, default="Nil")
    hemat_symp = models.TextField(
        'Haematological', max_length=500, default="Nil")
    immuno_symp = models.TextField(
        'Immunologic/ Allergic', max_length=500, default="Nil")

    admission_detail = models.ForeignKey(AdmissionDetail)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=True)

    def __unicode__(self):
        return '''%s \n %s \n
              %s \n %s \n %s \n 
              %s \n %s \n %s \n 
              %s \n %s \n %s \n
              %s \n %s \n %s \n %s
           ''' % (self.const_symp,
                  self.eye_symp,
                  self.ent_symp,
                  self.cvs_symp,
                  self.resp_symp,
                  self.gi_symp,
                  self.gu_symp,
                  self.ms_symp,
                  self.integ_symp,
                  self.neuro_symp,
                  self.psych_symp,
                  self.endocr_symp,
                  self.hemat_symp,
                  self.immuno_symp,
                  self.created_at.date().isoformat())

    class Meta:
        verbose_name = "Admission Review of Systems"
        verbose_name_plural = "Admission Review of Systems"


class AdmissionInv(AuShadhaBaseModel):

    def __init__(self, *args, **kwargs):
      self.__model_label__ = "inv"
      self._parent_model = 'admission_detail'    

    investigation = models.ForeignKey(LabInvestigationRegistry)
    value = models.CharField('Findings', max_length=30)
    admission_detail = models.ForeignKey(AdmissionDetail)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __unicode__(self):
        return "%s: %s \n(%s)" % (self.investigation, self.value, self.created_at.date().isoformat())

    class Meta:
        verbose_name = "Lab Investigation"
        verbose_name_plural = "Lab Investigation"
        ordering = ('admission_detail', 'created_at', 'investigation')



class AdmissionDetailForm(AuShadhaBaseModelForm):
    
    __form_name__ = "Admission Detail Form"
    
    admitting_physician = ModelChoiceField(
        queryset=Staff.objects.filter(clinic_staff_role='doctor'))

    dijit_fields = ADMISSION_DETAIL_FORM_CONSTANTS

    class Meta:
        model = AdmissionDetail
        exclude = DEFAULT_ADMISSION_DETAIL_FORM_EXCLUDES


class AdmissionComplaintAddForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission Complaint Form"
    
    dijit_fields = ADMISSION_COMPLAINTS_FORM_CONSTANTS


    class Meta:
        model = AdmissionComplaint
        exclude = ('admission_detail','patient_detail')


class AdmissionComplaintEditForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission Complaint Form"
    
    dijit_fields = ADMISSION_COMPLAINTS_FORM_CONSTANTS

    class Meta:
        model = AdmissionComplaint
        exclude = ('admission_detail','patient_detail')


class AdmissionHPIForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission HPI Form"
    
    dijit_fields = ADMISSION_HPI_FORM_CONSTANTS

    class Meta:
        model = AdmissionHPI
        exclude = ('admission_detail','patient_detail')


class AdmissionPastHistoryForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission Past History Form"
    
    dijit_fields = ADMISSION_PAST_HISTORY_FORM_CONSTANTS

    class Meta:
        model = AdmissionPastHistory
        exclude = ('admission_detail','patient_detail')


class AdmissionImagingForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission Imaging Form"
    
    dijit_fields = ADMISSION_IMAGING_FORM_CONSTANTS

    class Meta:
        model = AdmissionImaging
        exclude = ('admission_detail','patient_detail')



class AdmissionInvForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission Investigation Form"
    
    dijit_fields = ADMISSION_INVESTIGATION_FORM_CONSTANTS

    class Meta:
        model = AdmissionInv
        exclude = ('admission_detail','patient_detail')


class AdmissionROSForm(AuShadhaBaseModelForm):

    __form_name__ = "Admission ROS Form"

    dijit_fields = ADMISSION_ROS_FORM_CONSTANTS
    
    class Meta:
        model = AdmissionROS
        exclude = ('admission_detail', 'parent_clinic', 'created_at')
