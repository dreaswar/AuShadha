#
# Physical Examination Models for AuShadha
# Takes care of all the Physical Examination Related Data.
# Author    : Dr.Easwar T.R
# Copyright : 2012
# Date      : 2012-12-31
# Licence   : GNU-GPL Version 3
#

# General Imports
import datetime
from datetime import date, time, datetime

# General Django Imports
from django.db import models
from django.forms           import ModelForm,\
    Textarea,\
    CharField,\
    Widget,\
    TextInput,\
    HiddenInput,\
    ModelChoiceField

from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError


# Application specific django imports::

from aushadha_base_models.models import AuShadhaBaseModel
from aushadha_users.models import AuShadhaUser
from physician.models import *
from clinic.models import Clinic, Staff

from patient.models import *
from admission.models import *
from visit.models import VisitDetail


# Imports the needed Constants
from phyexam.phyexam_constants import *

from dijit_fields_constants import VITAL_FORM_CONSTANTS, \
    GEN_EXAM_FORM_CONSTANTS, \
    SYS_EXAM_FORM_CONSTANTS, \
    NEURO_EXAM_FORM_CONSTANTS,\
    VASCULAR_EXAM_FORM_CONSTANTS

# Constants

DEFAULT_VITALS = {
    'sys_bp': 120,
    'dia_bp': 80,
    'pulse_rate': 80,
    'resp_rate': 20,
    'gcs': 15,
    'height': 0.00,
    'weight': 0.00,
    'bmi': 0.00,
    'remarks': "NAD"
}

DEFAULT_PHYEXAM_FORM_EXCLUDES = ('phy_exam_base_model',
                                 'physician',
                                 'visit_detail',
                                 'admission_detail',
                                 'remarks'
                                 )


# Physical Examination Models start here:::
# NEW PHYEXAM MODELS ###############################
class PhyExamBaseModel(AuShadhaBaseModel):
    __model_label__ = 'phy_exam'

    remarks = models.TextField(
        blank=True, null=True, default="NAD", max_length=200)
    created_at = models.DateTimeField(
        auto_now=True, auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=True)

    admission_detail = models.ForeignKey(
        'admission.Admission', null=True, blank=True)
    visit_detail = models.ForeignKey(
        'visit.VisitDetail', null=True, blank=True)
    physician = models.ForeignKey('clinic.Staff')

    base_model = models.OneToOneField(
        'aushadha_base_models.AuShadhaBaseModel', parent_link=True)

    def save(self, *args, **kwargs):
        if self.physician in Staff.objects.filter(clinic_staff_role='doctor'):
            if self.admission_detail or self.visit_detail:
                super(PhyExamBaseModel, self).save(*args, **kwargs)
            else:
                raise Exception(
                    "You Require either an Admission / Visit to add an exam to..")
        else:
            raise Exception(
                "You need to belong to Role - Doctor to save an examination !")

    def __unicode__(self):
        if self.admission_detail:
            return "Adm: %s, Date: %s" % (self.admission_detail, self.created_at)
        elif self.visit_detail:
            return "Visit: %s, Date: %s" % (self.visit_detail, self.created_at)
        else:
            return "Created at: %s" % (self.created_at)


class VitalExam_FreeModel(PhyExamBaseModel):
    sys_bp = models.PositiveIntegerField(
        'Systolic B.P', max_length=3, default=120)
    dia_bp = models.PositiveIntegerField(
        'Diastolic B.P', max_length=3, default=80)
    pulse_rate = models.PositiveIntegerField(
        'Pulse Rate', max_length=3, default=82)
    resp_rate = models.PositiveIntegerField(
        'Respiratory Rate', max_length=2, default=20)

    gcs = models.PositiveIntegerField(
        'GCS', max_length=2, default=15)

    height = models.PositiveIntegerField(
        max_length=3, null=True, blank=True)
    weight = models.PositiveIntegerField(
        max_length=3, null=True, blank=True)
    bmi = models.DecimalField('BMI', decimal_places=2, max_digits=4)

    phy_exam_base_model = models.OneToOneField(
        'PhyExamBaseModel', parent_link=True)

    def __init__(self, *args, **kwargs):
        self.__model_label__ = 'vital'
        super(VitalExam_FreeModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__model_label__ = 'vital'
        super(VitalExam_FreeModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Vital"
        verbose_name = "Vital"
        ordering = ['sys_bp', 'dia_bp', 'pulse_rate',
                    'resp_rate', 'height', 'weight', 'bmi', 'gcs']


class GenExam_FreeModel(PhyExamBaseModel):
    __model_label__ = 'gen_exam'

    pallor = models.BooleanField(default=False)
    icterus = models.BooleanField(default=False)
    cyanosis = models.BooleanField(default=False)
    clubbing = models.BooleanField(default=False)
    lymphadenopathy = models.BooleanField(default=False)
    edema = models.BooleanField(default=False)
    phy_exam_base_model = models.OneToOneField(
        'PhyExamBaseModel', parent_link=True)

    def __init__(self, *args, **kwargs):
        self.__model_label__ = 'gen_exam'
        super(GenExam_FreeModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__model_label__ = 'gen_exam'
        super(GenExam_FreeModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "General Examination"
        verbose_name = "General Examination"
        ordering = ['pallor', 'icterus', 'cyanosis',
                    'clubbing', 'lymphadenopathy', 'edema']


class SysExam_FreeModel(PhyExamBaseModel):
    __model_label__ = 'sys_exam'

    heent = models.TextField(max_length=75, default=HEENT_EX)
    cns = models.TextField(max_length=100, default=CNS_EX)
    cvs = models.TextField(max_length=100, default=CVS_EX)
    respiratory_system = models.TextField(
        max_length=100, default=RESP_EX)
    git_and_gut = models.TextField(
        max_length=100, default=GIT_GUT_EX)
    phy_exam_base_model = models.OneToOneField(
        'PhyExamBaseModel', parent_link=True)

    def __init__(self, *args, **kwargs):
        self.__model_label__ = 'sys_exam'
        super(SysExam_FreeModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__model_label__ = 'sys_exam'
        super(SysExam_FreeModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "System Examination"
        verbose_name = "System Examination"
        ordering = ['heent', 'cns', 'cvs', 'respiratory_system', 'git_and_gut']


class PeriNeuroExam_FreeModel(PhyExamBaseModel):

    __model_label__ = 'neuro_exam'

    plantar = models.TextField('Plantar Reflex',
                               max_length=30,
                               default="Bilateral Flexor response",
                                       help_text='limit to 30 words')

    abdominal = models.TextField('Abdominal Reflex',
                                 max_length=30,
                                 default="Ellicited well in all four quadrants",
                                 help_text='limit to 30 words'
                                 )

    cremasteric = models.TextField(max_length=30, default="Present")

    anal_wink = models.TextField(max_length=30, default="Present")

    motor = models.TextField('Motor Exam',
                             max_length=100,
                             default="Normal Bulk, Tone and Power in all four limbs. No Fasciculations.",
                             help_text='limit to 100 words')

    sensory = models.TextField('Sensory Exam',
                               max_length=100,
                               default="Normal Sensation in all four limbs. Perianal sensation intact",
                                       help_text='limit to 100 words')

    dtr = models.TextField('Deep Tendon Reflex',
                           max_length=50,
                           default="Equally ellicitable in all four limbs. No Clonus.",
                           help_text='limit to 50 words'
                           )

    cranial_nerve = models.TextField('Cranial Nerve Exam',
                                     max_length=30,
                                     default="All Cranial Nerves NAD",
                                     help_text='limit to 30 words')

    class Meta:
        verbose_name_plural = "Neuro Examination"
        verbose_name = "Neuro Examination"

    def __init__(self, *args, **kwargs):
        self.__model_label__ = 'neuro_exam'
        super(PeriNeuroExam_FreeModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__model_label__ = 'neuro_exam'
        super(PeriNeuroExam_FreeModel, self).save(*args, **kwargs)


class VascExam_FreeModel(PhyExamBaseModel):

    __model_label__ = 'vascular_exam'

#  pulse      = models.BooleanField()
    location = models.CharField(
        max_length=20, choices=(('DP', "Dorsalis Pedis"),
                               ("PT", "Posterior Tibial"),
                               ('P', "Popliteal"),
                               ('F', "Femoral"),
                               ('SC', "Sub-Clavian"),
                               ('A', "Axillary"),
                               ('B', "Brachial"),
                               ('R', "Radial"),
                               ('U', "Ulnar")
                                )
    )
    side = models.CharField(
        max_length=10, choices=EXAMINATION_SIDES, default='Right')
    character = models.CharField(max_length=20,
                                 choices=(('bounding', 'Bounding'),
                                          ('normal', 'Normal'),
                                          ('weak', 'Weak'),
                                          ('absent', "Absent")
                                          ),
                                 default = 'Normal'
                                 )

    class Meta:
        verbose_name_plural = "Vascular Examination"
        verbose_name = "Vascular Examination"

    def __init__(self, *args, **kwargs):
        self.__model_label__ = 'vascular_exam'
        super(VascExam_FreeModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__model_label__ = 'vascular_exam'
        super(VascExam_FreeModel, self).save(*args, **kwargs)


# NEW MODEL FORMS ###############################
class PhyExamBaseModelForm(ModelForm):

    """Base class for all Physical Examination Forms."""
    dijit_fields = []

    __form_name__ = "Physical Examination Base Form"

    class Meta:
        model = PhyExamBaseModel
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES

    def __init__(self, *args, **kwargs):
        super(PhyExamBaseModelForm, self).__init__(*args, **kwargs)
        self.generate_dijit_form()

    def generate_dijit_form(self):
        if self.dijit_fields:
            for field_name, value_dict in self.dijit_fields.iteritems():
                for prop_key, prop_val in value_dict.iteritems():
                    self.fields[field_name].widget.attrs[prop_key] = prop_val
        else:
            print "No Text Fields ! "
            raise Exception("No Dijisable Dictionary Supplied")


class VitalExam_FreeModelForm(PhyExamBaseModelForm):

    """Describes the Vital Monitoring signs ModelForm."""
    __form_name__ = "Vital Signs Form"

    dijit_fields = VITAL_FORM_CONSTANTS

    class Meta:
        model = VitalExam_FreeModel
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class GenExam_FreeModelForm(PhyExamBaseModelForm):

    """Describes the General Exam Monitoring ModelForm."""
    __form_name__ = "General Examination Form"

    dijit_fields = GEN_EXAM_FORM_CONSTANTS

    class Meta:
        model = GenExam_FreeModel
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class SysExam_FreeModelForm(PhyExamBaseModelForm):

    """Describes the Systemic Exam Monitoring ModelForm."""
    __form_name__ = "Systemic Examination Form"

    dijit_fields = SYS_EXAM_FORM_CONSTANTS

    class Meta:
        model = SysExam_FreeModel
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class PeriNeuroExam_FreeModelForm(PhyExamBaseModelForm):

    """Describes the Neurological Exam Monitoring ModelForm."""
    __form_name__ = "Neurological Examination Form"

    dijit_fields = NEURO_EXAM_FORM_CONSTANTS

    class Meta:
        model = PeriNeuroExam_FreeModel
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class VascExam_FreeModelForm(PhyExamBaseModelForm):

    """Describes the Vascular Exam Monitoring ModelForm."""
    __form_name__ = "Vascular Examination Form"

    dijit_fields = VASCULAR_EXAM_FORM_CONSTANTS

    class Meta:
        model = VascExam_FreeModel
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


#
#
# NON FREE MODELS & FORMS.
# These are bound to specific PhyExam Parent.
#   This PhyExam Parent needs to be created first.
# Hence the name of the new mode is _FreeModel, where user can add exams directly to
#   Visits / Admission.
# The dijitisation is also repetitive and spaghetti code.
#   This will be phased out very soon.
# Several view codes depends on these now.  So its left in place
#
class PhyExam(AuShadhaBaseModel):

    consult_nature = models.CharField(
        max_length=20, choices=CONSULT_CHOICES)

    has_vital = models.BooleanField(default=False, editable=False)
    has_gen = models.BooleanField(default=False, editable=False)
    has_sys = models.BooleanField(default=False, editable=False)
    has_neuro = models.BooleanField(default=False, editable=False)
    has_vasc = models.BooleanField(default=False, editable=False)

    created_at = models.DateTimeField(
        auto_now=True, auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=True)

    admission_detail = models.ForeignKey(
        'admission.Admission', null=True, blank=True)
    visit_detail = models.ForeignKey(
        'visit.VisitDetail', null=True, blank=True)
    physician = models.ForeignKey('clinic.Staff')

    class Meta:
        verbose_name_plural = "Physical Examination"
        verbose_name = "Physical Examination"
        unique_together = (
            ('admission_detail', 'created_at'), ('visit_detail', 'created_at'))
        ordering = [
            'created_at', 'admission_detail', 'visit_detail', 'physician']

    def __unicode__(self):
        return "ID: %s, Date: %s, Time: %s Nature:%s" % (self.id,
                                                         self.created_at.date(
                                                         ),
                                                         self.created_at.time(
                                                         ),
                                                         self.consult_nature
                                                         )

    def __trimmed_unicode__(self):
        return "%s : %s -- %s" % (self.created_at.date().isoformat(),
                                  datetime.datetime.strftime(
                                      self.created_at, "%H:%M:%S"),
                                  self.consult_nature
                                  )

    def has_others(self, id):
        id = self.id
        try:
            pe_obj = PhyExam.objects.get(pk=id)
        except(ValueError, AttributeError, TypeError, PhyExam.DoesNotExist):
            return False
        vital_obj = VitalExam.objects.filter(phyexam=pe_obj)
        gen_obj = GenExam.objects.filter(phyexam=pe_obj)
        sys_obj = SysExam.objects.filter(phyexam=pe_obj)
        reg_obj = RegExam.objects.filter(phyexam=pe_obj)
        neuro_obj = PeriNeuroExam.objects.filter(phyexam=pe_obj)
        vasc_obj = VascExam.objects.filter(phyexam=pe_obj)

        if vital_obj:
            self.has_vital = True
        else:
            self.has_vital = False

        if gen_obj:
            self.has_gen = True
        else:
            self.has_gen = False

        if sys_obj:
            self.has_sys = True
        else:
            self.has_sys = False

        if reg_obj:
            self.has_reg = True
        else:
            self.has_reg = False

        if neuro_obj:
            self.has_neuro = True
        else:
            self.has_neuro = False

        if vasc_obj:
            self.has_vasc = True
        else:
            self.has_vasc = False

    def save(self, *args, **kwargs):
        self.__model_label__ = "phyexam"

        if self.visit_detail:
            if self.admission_detail:
                raise ValidationError('''The Item is already attached to an Admission.
                                  Cannot attach it to a visit.
                                  Please add a new exam
                               '''
                                      )
            else:
                super(PhyExam, self).save(*args, **kwargs)
        elif self.admission_detail:
            if self.visit_detail:
                raise ValidationError('''The Item is already attached to a Visit.
                                  Cannot attach it to an Admission.
                                  Please add a new exam
                               ''')
            else:
                self.has_others(self.id)
                super(PhyExam, self).save(*args, **kwargs)
        else:
            return False

    def get_edit_url(self):
        return '/AuShadha/phyexam/edit/%s/' % (self.id)

    def get_del_url(self):
        return '/AuShadha/phyexam/del/%s/' % (self.id)

    def get_phyexam_copy_to_url(self, copy_to):
        return 'AuShadha/phyexam/copy_to/%s/%s/' % (copy_to, self.id)

    def get_phyexam_add_other_exams_url(self):
        return 'AuShadha/phyexam/add_other_exams/%s/' % (self.id)


class VitalExam(AuShadhaBaseModel):
    sys_bp = models.PositiveIntegerField(
        'Systolic B.P', max_length=3, default=120)
    dia_bp = models.PositiveIntegerField(
        'Diastolic B.P', max_length=3, default=80)
    pulse_rate = models.PositiveIntegerField(
        'Pulse Rate', max_length=3, default=82)
    resp_rate = models.PositiveIntegerField(
        'Respiratory Rate', max_length=2, default=20)

    gcs = models.PositiveIntegerField(max_length=2, default=15)

    height = models.PositiveIntegerField(
        max_length=3, null=True, blank=True, help_text="Height in cms.")
    weight = models.PositiveIntegerField(
        max_length=3, null=True, blank=True, help_text="Weight in kgs.")
    bmi = models.DecimalField(decimal_places=2, max_digits=4)

    remarks = models.TextField(
        blank=True, null=True, default="NAD", max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    phyexam = models.ForeignKey(PhyExam, null=True, blank=True)

    def __unicode__(self):
        return "%s/%s mmHg" % (self.sys_bp, self.dia_bp)

    class Meta:
        verbose_name_plural = "Vital"
        verbose_name = "Vital"
        unique_together = (('date_time', 'phyexam'),)
        ordering = ['phyexam', 'date_time']


class GenExam(AuShadhaBaseModel):
    pallor = models.BooleanField(default=False)
    icterus = models.BooleanField(default=False)
    cyanosis = models.BooleanField(default=False)
    clubbing = models.BooleanField(default=False)
    lymphadenopathy = models.BooleanField(default=False)
    edema = models.BooleanField(default=False)
    remarks = models.TextField(
        blank=True, null=True, default="NAD", max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    phyexam = models.ForeignKey(PhyExam, null=True, blank=True)
    #created_at        = models.DateTimeField(auto_now = True, auto_now_add = True, editable=False)
    #modified_at       = models.DateTimeField(auto_now = True, editable=True)

    #admission_detail  = models.ForeignKey('admission.Admission'  ,null = True, blank = True)
    #visit_detail      = models.ForeignKey('visit.VisitDetail'    ,null = True, blank = True)
    #physician         = models.ForeignKey('clinic.Staff')

    def __unicode__(self):
        if self.admission_detail:
            return "Adm: %s, Pat: %s, Date: %s" % (self.phyexam.admission_detail.date_of_admission,
                                                   self.phyexam.admission_detail.patient_detail,
                                                   self.created_at)
        elif self.visit_detail:
            return "Visit: %s, Pat: %s, Date: %s" % (self.phyexam.visit_detail.visit_date,
                                                     self.phyexam.visit_detail.patient_detail,
                                                     self.created_at)
        else:
            return "%s %s - %s" % (self.created_at, self.modified_at, self.physician)

    class Meta:
        verbose_name_plural = "General Examination"
        verbose_name = "General Examination"
        unique_together = (('date_time', 'phyexam'),)
        ordering = ['phyexam', 'date_time']


#

class SysExam(AuShadhaBaseModel):

    heent = models.TextField(max_length=75, default=HEENT_EX)
    cns = models.TextField(max_length=100, default=CNS_EX)
    cvs = models.TextField(max_length=100, default=CVS_EX)
    respiratory_system = models.TextField(
        max_length=100, default=RESP_EX)
    git_and_gut = models.TextField(
        max_length=100, default=GIT_GUT_EX)
    date_time = models.DateTimeField(auto_now=True)
    phyexam = models.ForeignKey(PhyExam, null=True, blank=True)

    def __unicode__(self):
        return "Adm: %s, Pat: %s, Date: %s" % (self.phyexam.admission_detail.date_of_admission,
                                               self.phyexam.admission_detail.patient_detail,
                                               self.phyexam)

    class Meta:
        verbose_name_plural = "System Examination"
        verbose_name = "System Examination"
        unique_together = (('date_time', 'phyexam'),)
        ordering = ['phyexam', 'date_time']


class PeriNeuroExam(AuShadhaBaseModel):

    plantar = models.TextField('Plantar Reflex',
                               max_length=30,
                               default="Bilateral Flexor response",
                                       help_text='limit to 30 words')

    abdominal = models.TextField('Abdominal Reflex',
                                 max_length=30,
                                 default="Ellicited well in all four quadrants",
                                 help_text='limit to 30 words'
                                 )

    cremasteric = models.TextField(max_length=30, default="Present")

    anal_wink = models.TextField(max_length=30, default="Present")

    motor = models.TextField('Motor Exam',
                             max_length=100,
                             default="Normal Bulk, Tone and Power in all four limbs. No Fasciculations.",
                             help_text='limit to 100 words')

    sensory = models.TextField('Sensory Exam',
                               max_length=100,
                               default="Normal Sensation in all four limbs. Perianal sensation intact",
                                       help_text='limit to 100 words')

    dtr = models.TextField('Deep Tendon Reflex',
                           max_length=50,
                           default="Equally ellicitable in all four limbs. No Clonus.",
                           help_text='limit to 50 words'
                           )

    cranial_nerve = models.TextField('Cranial Nerve Exam',
                                     max_length=30,
                                     default="All Cranial Nerves NAD",
                                     help_text='limit to 30 words')

    remarks = models.TextField(max_length=75,
                               default="No Long tract signs.\nRomberg/ Finger Nose/ Adiadokokinesia Negative",
                                       help_text='limit to 75 words')

    date_time = models.DateTimeField(auto_now=True)
    phyexam = models.ForeignKey(PhyExam, null=True, blank=True)

    def __unicode__(self):
        return "Adm: %s, Pat: %s, Date: %s" % (self.phyexam.admission_detail.date_of_admission,
                                               self.phyexam.admission_detail.patient_detail,
                                               self.phyexam)

    class Meta:
        verbose_name_plural = "Perpheral Neuro Examination"
        verbose_name = "Peripheral Neuro Examination"
        unique_together = (('date_time', 'phyexam'),)
        ordering = ['phyexam', 'date_time']


class VascExam(AuShadhaBaseModel):
#  pulse      = models.BooleanField()
    location = models.CharField(
        max_length=20, choices=(('DP', "Dorsalis Pedis"),
                               ("PT", "Posterior Tibial"),
                               ('P', "Popliteal"),
                               ('F', "Femoral"),
                               ('SC', "Sub-Clavian"),
                               ('A', "Axillary"),
                               ('B', "Brachial"),
                               ('R', "Radial"),
                               ('U', "Ulnar")
                                )
    )
    side = models.CharField(
        max_length=10, choices=EXAMINATION_SIDES, default='Right')
    character = models.CharField(max_length=20,
                                 choices=(('bounding', 'Bounding'),
                                          ('normal', 'Normal'),
                                          ('weak', 'Weak'),
                                          ('absent', "Absent")
                                          ),
                                 default = 'Normal'
                                 )

    remarks = models.TextField(max_length=100,
                               default="""No Regional Varicosity / No Oedema or Compartment tension.
                                                 No clinical signs of DVT. No Skin Ulcers
                                              """,
                               help_text='limit to 100 words')

    date_time = models.DateTimeField(auto_now=True)
    phyexam = models.ForeignKey(PhyExam, null=True, blank=True)

    def __unicode__(self):
        return "Adm: %s, Pat: %s, Date: %s" % (self.phyexam.admission_detail.date_of_admission,
                                               self.phyexam.admission_detail.patient_detail,
                                               self.phyexam)

    class Meta:
        verbose_name_plural = "Vascular Examination"
        verbose_name = "Vascular Examination"
        unique_together = (('date_time', 'phyexam'))
        ordering = ['location', 'side', 'phyexam', 'date_time']


#
#
# Dijitsed Examination Forms
#
#
class VascExamForm(ModelForm):

    class Meta:
        model = VascExam
        exclude = ('parent_clinic', 'phyexam')

    def __init__(self, *args, **kwargs):
        super(VascExamForm, self).__init__(*args, **kwargs)
        text_fields = [{"field": 'location',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'side',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'character',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'remarks',
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'date_time',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false, 'disabled': true"
                        }
                       ]
        for field in text_fields:
            print(self.fields[field['field']].widget)
            self.fields[field['field']].widget.attrs[
                'data-dojo-type'] = field['data-dojo-type']
            self.fields[field['field']].widget.attrs[
                'data-dojo-props'] = field['data-dojo-props']
            self.fields[field['field']].widget.attrs[
                'max_length'] = field['max_length']


class PeriNeuroExamForm(ModelForm):

    class Meta:
        model = PeriNeuroExam
        exclude = ('parent_clinic', 'phyexam')

    def __init__(self, *args, **kwargs):
        super(PeriNeuroExamForm, self).__init__(*args, **kwargs)
        text_fields = [{"field": 'plantar',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'abdominal',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'cremasteric',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'anal_wink',
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'motor',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'sensory',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'dtr',
                        'max_length': 50,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'remarks',
                        'max_length': 75,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'date_time',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false, 'disabled': true"
                        }
                       ]
        for field in text_fields:
            print(self.fields[field['field']].widget)
            self.fields[field['field']].widget.attrs[
                'data-dojo-type'] = field['data-dojo-type']
            self.fields[field['field']].widget.attrs[
                'data-dojo-props'] = field['data-dojo-props']
            self.fields[field['field']].widget.attrs[
                'max_length'] = field['max_length']


class SysExamForm(ModelForm):

    class Meta:
        model = SysExam
        exclude = ('parent_clinic', 'phyexam')

    def __init__(self, *args, **kwargs):
        super(SysExamForm, self).__init__(*args, **kwargs)
        text_fields = [{"field": 'heent',
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'cns',
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'cvs',
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'respiratory_system',
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'git_and_gut',
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'date_time',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false, 'disabled': true"
                        }
                       ]
        for field in text_fields:
            print(self.fields[field['field']].widget)
            self.fields[field['field']].widget.attrs[
                'data-dojo-type'] = field['data-dojo-type']
            self.fields[field['field']].widget.attrs[
                'data-dojo-props'] = field['data-dojo-props']
            self.fields[field['field']].widget.attrs[
                'max_length'] = field['max_length']


class GenExamForm(ModelForm):

    class Meta:
        model = GenExam
        exclude = ('parent_clinic', 'phyexam')

    def __init__(self, *args, **kwargs):
        super(GenExamForm, self).__init__(*args, **kwargs)
        text_fields = [{"field": 'pallor',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'icterus',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'cyanosis',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'clubbing',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'lymphadenopathy',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'edema',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'remarks',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'date_time',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false, 'disabled': true"
                        }
                       ]
        for field in text_fields:
            print(self.fields[field['field']].widget)
            self.fields[field['field']].widget.attrs[
                'data-dojo-type'] = field['data-dojo-type']
            self.fields[field['field']].widget.attrs[
                'data-dojo-props'] = field['data-dojo-props']
            self.fields[field['field']].widget.attrs[
                'max_length'] = field['max_length']


class VitalExamForm(ModelForm):

    class Meta:
        model = VitalExam
        exclude = ('phyexam',)

    def __init__(self, *args, **kwargs):
        super(VitalExamForm, self).__init__(*args, **kwargs)
        text_fields = [{"field": 'sys_bp',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :true"
                        },
                       {"field": 'dia_bp',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :true"
                        },
                       {"field": 'pulse_rate',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'resp_rate',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'gcs',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'height',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' :false"
                        },
                       {"field": 'weight',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :false,placeHolder:'Any other Classification..'"
                        },
                       {"field": 'remarks',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : false"
                        },
                       {"field": 'date_time',
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : false, 'disabled': true"
                        }
                       ]
        for field in text_fields:
            print(self.fields[field['field']].widget)
            self.fields[field['field']].widget.attrs[
                'data-dojo-type'] = field['data-dojo-type']
            self.fields[field['field']].widget.attrs[
                'data-dojo-props'] = field['data-dojo-props']
            self.fields[field['field']].widget.attrs[
                'max_length'] = field['max_length']













# OLD FORMS AND MODELS ##
#
# Forms definition starts here:::
#


# def set_up_phyexam_form(form_instance):
    # text_fields = [
                 #{"field"         : 'admission_detail',
                    #'max_length'    :  ''         ,
                    #"data-dojo-type": "dijit.form.Select",
                    #"data-dojo-id"  : "admission_phyexam_admission_detail",
                    #"data-dojo-props": r" 'required':'true', 'readOnly':'true'"
                    #},

                 #{"field"         : 'physician',
                    #'max_length'    :  '100'         ,
                    #"data-dojo-type": "dijit.form.Select",
                    #"data-dojo-id"  : "admission_phyexam_physician",
                    # "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
                    #},

                    #{"field"         : 'consult_nature',
                    #'max_length'    :  '100'         ,
                    #"data-dojo-type": "dijit.form.Select",
                    #"data-dojo-id"  : "admission_phyexam_consult_nature",
                    #"data-dojo-props": r"'required' : 'true' , 'readOnly':'true'"
                    #},
            #]

    # for field in text_fields:
        # print(form_instance.fields[field['field']].widget);
        #form_instance.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
        #form_instance.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
        #form_instance.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
        #form_instance.fields[field['field']].widget.attrs['max_length']      = field['max_length']


#
# IP Physical Exam forms..
#

# class PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('visit_detail')

    # def __init__(self, *args, **kwargs):
        #super(PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)


# class IP_Initial_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('visit_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Initial_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)

# class IP_Fu_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('visit_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Fu_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)

# class IP_Pre_Op_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('visit_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Pre_Op_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)

# class IP_Post_Op_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('visit_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Post_Op_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)

# class IP_Discharge_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('visit_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Discharge_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)


#
# OP Physical Exam forms..
#

# class OP_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('admission_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Initial_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)


# class OP_Initial_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('admission_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Initial_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)

# class OP_Fu_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('admission_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Initial_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)


# class OP_Dis_PhyExamForm(ModelForm):
    #physician = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))
    # class Meta:
        #model   = PhyExam
        #exclude = ('admission_detail')

    # def __init__(self, *args, **kwargs):
        #super(IP_Initial_PhyExamForm, self).__init__(*args, **kwargs)
        #self.set_up = set_up_phyexam_form(self)


#
# Other Exam Forms - In Patient
#

# class VitalForm(ModelForm):

    # class Meta:
        #model  = VitalExam
        #exclude =('phyexam','visit_detail')

# class GenExamForm(ModelForm):

    # class Meta:
        #model  = GenExam
        #exclude = ('phyexam','visit_detail')
        #widgets = {'remarks':Textarea(attrs={'cols':80, 'rows':5})}


# class SysExamForm(ModelForm):

    # class Meta:
        #model  = SysExam
        #exclude = ('phyexam','visit_detail')
        # widgets = {'remarks'         :Textarea(attrs={'cols':80, 'rows':5}),
                    #'heent'             :Textarea(attrs={'cols':80, 'rows':5}),
                    #'cns'               :Textarea(attrs={'cols':80, 'rows':5}),
                    #'cvs'               :Textarea(attrs={'cols':80, 'rows':5}),
                    #'respiratory_system':Textarea(attrs={'cols':80, 'rows':5}),
                    #'git_and_gut'       :Textarea(attrs={'cols':80, 'rows':5}),
                    #}

# class PeriNeuroExamForm(ModelForm):

    # class Meta:
        #model   = PeriNeuroExam
        #exclude = ('phyexam','visit_detail')
        # widgets = {'remarks'      :Textarea(attrs={'cols':80, 'rows':5}),
                    #'motor'         :Textarea(attrs={'cols':80, 'rows':5}),
                    #'sensory'       :Textarea(attrs={'cols':80, 'rows':5}),
                    #'dtr'           :Textarea(attrs={'cols':80, 'rows':5}),
                    #'plantar'       :Textarea(attrs={'cols':80, 'rows':5}),
                    #'abdominal'     :Textarea(attrs={'cols':80, 'rows':5}),
                    #'cremasteric'   :Textarea(attrs={'cols':80, 'rows':5}),
                    #'anal_wink'     :Textarea(attrs={'cols':80, 'rows':5}),
                    #'cranial_nerve' :Textarea(attrs={'cols':80, 'rows':5}),
                    #}

# class VascExamForm(ModelForm):

    # class Meta:
        #model   = VascExam
        #exclude = ('phyexam','visit_detail')
        #widgets = {'remarks':Textarea(attrs={'cols':80, 'rows':5}),}


#
# Other Exam Forms - Out Patient
#

# class OP_VitalForm(ModelForm):

    # class Meta:
        #model  = VitalExam
        #exclude =('phyexam','admission_detail')


# class OP_GenExamForm(ModelForm):

    # class Meta:
        #model  = GenExam
        #exclude = ('phyexam','admission_detail')
        #widgets = {'remarks':Textarea(attrs={'cols':80, 'rows':5}),}


# class OP_SysExamForm(ModelForm):

    # class Meta:
        #model  = SysExam
        #exclude = ('phyexam','admission_detail')
        # widgets = {'remarks'           :Textarea(attrs={'cols':80, 'rows':5}),
                   #'heent'              :Textarea(attrs={'cols':80, 'rows':5}),
                   #'cns'                :Textarea(attrs={'cols':80, 'rows':5}),
                   #'cvs'                :Textarea(attrs={'cols':80, 'rows':5}),
                   #'respiratory_system' :Textarea(attrs={'cols':80, 'rows':5}),
                   #'git_and_gut'        :Textarea(attrs={'cols':80, 'rows':5}),
                    #}

# class OP_PeriNeuroExamForm(ModelForm):

    # class Meta:
        #model   = PeriNeuroExam
        #exclude = ('phyexam','admission_detail')
        # widgets = {'remarks'        :Textarea(attrs={'cols':80, 'rows':5}),
                     #'motor'          :Textarea(attrs={'cols':80, 'rows':5}),
                     #'sensory'        :Textarea(attrs={'cols':80, 'rows':5}),
                     #'dtr'            :Textarea(attrs={'cols':80, 'rows':5}),
                     #'plantar'        :Textarea(attrs={'cols':80, 'rows':5}),
                     #'abdominal'      :Textarea(attrs={'cols':80, 'rows':5}),
                     #'cremasteric'    :Textarea(attrs={'cols':80, 'rows':5}),
                     #'anal_wink'      :Textarea(attrs={'cols':80, 'rows':5}),
                     #'cranial_nerve'  :Textarea(attrs={'cols':80, 'rows':5}),
                    #}

# class OP_VascExamForm(ModelForm):

    # class Meta:
        #model   = VascExam
        #exclude = ('phyexam','admission_detail')
        #widgets = {'remarks':Textarea(attrs={'cols':80, 'rows':5})}
