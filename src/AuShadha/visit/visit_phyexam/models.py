################################################################################
# Physical Examination Models for AuShadha
# Takes care of all the Physical Examination Related Data.
# Author    : Dr.Easwar T.R
# Copyright : 2012
# Date      : 2012-12-31
# License   : GNU-GPL Version 3
################################################################################

# General Imports
import datetime
from datetime import date, time, datetime
import importlib
import yaml

# General Django Imports
from django.db import models
from django.forms import ModelForm,Textarea,CharField,Widget,TextInput,HiddenInput,ModelChoiceField
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError

# Application specific django imports::
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm
#from AuShadha.apps.aushadha_users.models import AuShadhaUser
#from AuShadha.apps.clinic.models import Clinic, Staff

#from physician.models import *
#from patient.models import PatientDetail
#from admission.models import AdmissionDetail
#from visit.models import VisitDetail

#PatientDetail  = UI.get_module("PatientRegistration")
#AdmissionDetail = UI.get_module("Admission")

VisitDetail = UI.get_module("OPD_Visit")


# Imports the needed Constants
from .phyexam_constants import *
from .phy_exam_constants import PC
from presentation_classes import vitalexamobjpresentationclass_factory,\
                                 genexamobjpresentationclass_factory,\
                                 sysexamobjpresentationclass_factory,\
                                 musexamobjpresentationclass_factory,\
                                 neuroexamobjpresentationclass_factory,\
                                 vascexamobjpresentationclass_factory,\
                                 vascexamobjpresentationclass_querysetfactory

from dijit_fields_constants import VITAL_FORM_CONSTANTS, \
                                    GEN_EXAM_FORM_CONSTANTS, \
                                    SYS_EXAM_FORM_CONSTANTS, \
                                    MUSCULOSKELETAL_EXAM_FORM_CONSTANTS,\
                                    NEURO_EXAM_FORM_CONSTANTS,\
                                    VASCULAR_EXAM_FORM_CONSTANTS,\
                                    PHY_EXAM_BASE_MODEL_FORM_CONSTANTS

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

DEFAULT_PHYEXAM_FORM_EXCLUDES = (
                                 'visit_detail',
                                 'remarks'
                                 )

VASC_EXAM_FORM_EXCLUDES = (
                          'visit_detail',
                          'remarks'
                          )


############################################################
# PHYEXAM MODELS 
############################################################

class PhyExamBaseModel(AuShadhaBaseModel):
    
    def __init__(self, *args, **kwargs):
      super(PhyExamBaseModel,self).__init__(*args, **kwargs)
      self.__model_label__ = "phyexam"
      self._parent_model = ['visit_detail',]

    remarks = models.TextField( blank=True, null=True, default="NAD", max_length=200)

    created_at = models.DateTimeField(auto_now=True, editable=False)

    modified_at = models.DateTimeField(auto_now=True, editable=True)

    visit_detail = models.ForeignKey('visit.VisitDetail', null=True, blank=True)

    #physician = models.ForeignKey(Staff)

    #base_model = models.OneToOneField('aushadha_base_models.AuShadhaBaseModel', parent_link=True)

    def __unicode__(self):
        return "Created at: %s" % (self.created_at)


class VitalExam(PhyExamBaseModel):

    def __init__(self, *args, **kwargs):
        super(VitalExam, self).__init__(*args, **kwargs)
        self.__model_label__ = "vital"
        self._parent_model = ['visit_detail',]

    sys_bp = models.PositiveIntegerField('Systolic B.P', max_length=3, default=120 , help_text="mmHg")
    dia_bp = models.PositiveIntegerField('Diastolic B.P', max_length=3, default=80, help_text="mmHg")
    pulse_rate = models.PositiveIntegerField('Pulse Rate', max_length=3, default=82, help_text="per min.")
    resp_rate = models.PositiveIntegerField('Respiratory Rate', max_length=2, default=20, help_text="per min.")
    gcs = models.PositiveIntegerField('GCS', max_length=2, default=15, help_text="out of 15")
    height = models.PositiveIntegerField(max_length=3, null=True, blank=True, help_text= "in Cms.")
    weight = models.PositiveIntegerField(max_length=3, null=True, blank=True, help_text="in Kg.")
    bmi = models.DecimalField('BMI', decimal_places=2, max_digits=4)
    temp = models.DecimalField('Temparature', decimal_places=2, max_digits=4, help_text="in Farenheit")
    phy_exam_base_model = models.OneToOneField('PhyExamBaseModel', parent_link=True)

    class Meta:
        verbose_name_plural = "Vital"
        verbose_name = "Vital"
        ordering = ['sys_bp', 
                    'dia_bp', 
                    'pulse_rate',
                    'resp_rate', 
                    'height', 
                    'weight', 
                    'bmi', 
                    'gcs'
                  ]

    def present(self):
        return vitalexamobjpresentationclass_factory( VitalExam.objects.get(pk = self.id) )

class GenExam(PhyExamBaseModel):

    def __init__(self, *args, **kwargs):
        super(GenExam, self).__init__(*args, **kwargs)
        self.__model_label__ = "gen"
        self._parent_model = ['visit_detail',]


    pallor = models.BooleanField(default=False)
    icterus = models.BooleanField(default=False)
    cyanosis = models.BooleanField(default=False)
    clubbing = models.BooleanField(default=False)
    lymphadenopathy = models.BooleanField(default=False)
    edema = models.BooleanField(default=False)
    phy_exam_base_model = models.OneToOneField('PhyExamBaseModel', parent_link=True)

    class Meta:
        verbose_name_plural = "General Examination"
        verbose_name = "General Examination"
        ordering = ['pallor', 'icterus', 'cyanosis',
                    'clubbing', 'lymphadenopathy', 'edema']

    def present(self):
        return genexamobjpresentationclass_factory( GenExam.objects.get(pk = self.id) )

class SysExam(PhyExamBaseModel):

    def __init__(self, *args, **kwargs):
        super(SysExam, self).__init__(*args, **kwargs)
        self.__model_label__ = 'sys'
        self._parent_model = ['visit_detail',]

    heent = models.TextField(max_length=1250, default=HEENT_EX)
    cns = models.TextField(max_length=1250, default=CNS_EX)
    cvs = models.TextField(max_length=1250, default=CVS_EX)
    respiratory_system = models.TextField(max_length=1250, default=RESP_EX)
    git_and_gut = models.TextField(max_length=1250, default=GIT_GUT_EX)
    phy_exam_base_model = models.OneToOneField('PhyExamBaseModel', parent_link=True)


    class Meta:
        verbose_name_plural = "System Examination"
        verbose_name = "System Examination"
        ordering = ['heent', 'cns', 'cvs', 'respiratory_system', 'git_and_gut']

    def present(self):
        return sysexamobjpresentationclass_factory( SysExam.objects.get(pk = self.id) )

class NeuroExam(PhyExamBaseModel):

    def __init__(self, *args, **kwargs):
        super(NeuroExam, self).__init__(*args, **kwargs)
        self.__model_label__ = 'neuro'
        self._parent_model = ['visit_detail',]

    plantar = models.TextField('Plantar Reflex',
                               max_length=100,
                               default="Bilateral Flexor response",
                                       help_text='limit to 30 words')

    abdominal = models.TextField('Abdominal Reflex',
                                 max_length=100,
                                 default="Ellicited well in all four quadrants",
                                 help_text='limit to 30 words'
                                 )

    cremasteric = models.TextField(max_length=100, default="Present")

    anal_wink = models.TextField(max_length=100, default="Present")

    motor = models.TextField('Motor Exam',
                             max_length=250,
                             default="Normal Bulk, Tone and Power in all four limbs. No Fasciculations",
                             help_text='limit to 100 words')

    sensory = models.TextField('Sensory Exam',
                               max_length=250,
                               default="Normal Sensation in all four limbs. Perianal sensation intact",
                                       help_text='limit to 100 words')

    dtr = models.TextField('Deep Tendon Reflex',
                           max_length=100,
                           default="Equally ellicitable in all four limbs. No Clonus",
                           help_text='limit to 50 words'
                           )

    cranial_nerve = models.TextField('Cranial Nerve Exam',
                                     max_length=100,
                                     default="All Cranial Nerves NAD",
                                     help_text='limit to 30 words')

    phy_exam_base_model = models.OneToOneField('PhyExamBaseModel', parent_link=True)


    class Meta:
        verbose_name_plural = "Neuro Examination"
        verbose_name = "Neuro Examination"

    def present(self):
        return neuroexamobjpresentationclass_factory( NeuroExam.objects.get(pk = self.id) )


class MusculoSkeletalExam(PhyExamBaseModel):

    def __init__(self, *args, **kwargs):
        super(MusculoSkeletalExam, self).__init__(*args, **kwargs)
        self.__model_label__ = 'musculoskeletal'
        self._parent_model = ['visit_detail',]

    ms_exam = models.TextField('Findings',
                               max_length=3000,
                               default = "NAD")

    phy_exam_base_model = models.OneToOneField('PhyExamBaseModel', parent_link=True)


    class Meta:
        verbose_name_plural = "Musculo Skeletal Examination"
        verbose_name = "Musculo Skeletal Examination"

    def present(self):
        return musexamobjpresentationclass_factory( MusculoSkeletalExam.objects.get(pk = self.id) )



class VascExam(PhyExamBaseModel):

    def __init__(self, *args, **kwargs):
        super(VascExam, self).__init__(*args, **kwargs)
        self.__model_label__ = 'vasc'
        self._parent_model = ['visit_detail',]

#  pulse      = models.BooleanField()
    location = models.CharField(max_length=20, 
                                choices=(('DP', "Dorsalis Pedis"),
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

    side = models.CharField(max_length=10, choices=EXAMINATION_SIDES, default='Right')

    character = models.CharField(max_length=20,
                                 choices=(('bounding', 'Bounding'),
                                          ('normal', 'Normal'),
                                          ('weak', 'Weak'),
                                          ('absent', "Absent")
                                          ),
                                 default = 'Normal'
                                 )

    phy_exam_base_model = models.OneToOneField('PhyExamBaseModel', parent_link=True)


    class Meta:
        verbose_name_plural = "Vascular Examination"
        verbose_name = "Vascular Examination"

    def present(self):
        return vascexamobjpresentationclass_factory( VascExam.objects.get(pk = self.id) )

##############################################################
# MODEL FORMS
##############################################################


class PhyExamBaseModelForm(ModelForm):

    """Base class for all Physical Examination Forms."""
    dijit_fields = PHY_EXAM_BASE_MODEL_FORM_CONSTANTS

    __form_name__ = "Physical Examination Base Form"

    class Meta:
        model = PhyExamBaseModel
        fields = "__all__"
        #exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES

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


class VitalExamForm(PhyExamBaseModelForm):

    """Describes the Vital Monitoring signs ModelForm."""
    __form_name__ = "Vital Signs Form"

    dijit_fields = VITAL_FORM_CONSTANTS

    class Meta:
        model = VitalExam
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class GenExamForm(PhyExamBaseModelForm):

    """Describes the General Exam Monitoring ModelForm."""
    __form_name__ = "General Examination Form"

    dijit_fields = GEN_EXAM_FORM_CONSTANTS

    class Meta:
        model = GenExam
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class SysExamForm(PhyExamBaseModelForm):

    """Describes the Systemic Exam Monitoring ModelForm."""
    __form_name__ = "Systemic Examination Form"

    dijit_fields = SYS_EXAM_FORM_CONSTANTS

    class Meta:
        model = SysExam
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class MusculoSkeletalExamForm(PhyExamBaseModelForm):

    """Describes the Musculoskeletal Exam Monitoring ModelForm."""
    __form_name__ = "Musculoskeletal Examination Form"

    dijit_fields = MUSCULOSKELETAL_EXAM_FORM_CONSTANTS

    class Meta:
        model = MusculoSkeletalExam
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES



class NeuroExamForm(PhyExamBaseModelForm):

    """Describes the Neurological Exam Monitoring ModelForm."""
    __form_name__ = "Neurological Examination Form"

    dijit_fields = NEURO_EXAM_FORM_CONSTANTS

    class Meta:
        model = NeuroExam
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES


class VascExamForm(PhyExamBaseModelForm):

    """Describes the Vascular Exam Monitoring ModelForm."""
    __form_name__ = "Vascular Examination Form"

    dijit_fields = VASCULAR_EXAM_FORM_CONSTANTS

    class Meta:
        model = VascExam
        exclude = DEFAULT_PHYEXAM_FORM_EXCLUDES
        #exclude = VASC_EXAM_FORM_EXCLUDES
