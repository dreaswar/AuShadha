##########################################################################
# PROJECT      : AuShadha
# Description  : visit_prescription Models
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
##########################################################################


import datetime
import yaml

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.clinic.models import Clinic, Staff

from .dijit_fields_constants import VISIT_PRESCRIPTION_FORM_CONSTANTS

DEFAULT_VISIT_PRESCRIPTION_FORM_EXCLUDES = ('visit_detail',)

VisitDetail = UI.get_module("OPD_Visit")

# Put all Models and ModelForms below this

ROUTE_CHOICES = (
    ('oral', "Oral"),
    ('sub_lingual', "Sub-Lingual"),
    ('intra_nasal', "Intra Nasal"),
    ('into_the_eye', "Into the Eye"),
    ('into_the_ear', "Into the Ear"),
    ('per_rectal', "Per Rectal"),
    ('per_vaginal', "Per Vaginal"),
    ('topical_application', "Topical Application"),
    ('intra_oral_application', "Intra Oral Application"),
    ('gargle', "Gargle"),
    ('sub_cutaneous', "Sub-Cutaneous"),
    ('intra_muscular', "Intra Muscular"),
    ('intra_muscular', "Intra Articular"),
    ('intra_osseous', "Intra Osseous"),
    ('intra_venous', "Intra Venous"),
    ('intra_arterial', "Intra Arterial"),
)


DISPENSING_FORM_CHOICES = (
    ('tablet', "Tablet"),
    ('dispersible_tablet', "Dispersible Tablet"),
    ('chewable_tablet', "Chewable Tablet"),
    ('capsule', "Capsule"),
    ('suspension', "Suspension"),
    ('dry_syrup', "Dry Syrup"),
    ('injection', "Injection"),
    ('spray', "Spray"),
    ('inhaler', "Inhaler"),
    ('gargle', 'Gargle'),
    ('drops', "Drops"),
    ('ointment', "Ointment"),
    ('gel', "Gel"),
    ('liniment', "Liniment"),
    ('suppository', "Suppository"),
)

ADMIN_FREQUENCY_CHOICES = (
    ('once_a_month', "Once a Month"),
    ('once_a_week', "Once a Week"),
    ('once_every_alternate_day', "Once every alternate Day"),
    ('once_a_day', "Once a Day"),
    ('every_twelth_hourly', "Every 12 Hours"),
    ('every_eight_hourly', "Every 8 Hours"),
    ('every_sixth_hourly', "Every 6 hours"),
    ('every_fourth_hourly', "Every 4 Hours"),
    ('every_two_hourly', "Every 2 Hours"),
    ('every_hour', "Every One Hour"),
    ('at_bed_time', "At Bed Time"),
    ('early_morning', "Early Morning"),
    ('after_noon', "After Noon"),
    ('sos', "S.O.S"),
    ('as_required', "As Needed"),
    ('stat', "Stat"),
)

DOSE_UNIT_CHOICES = (
    ('g', "gram"),
    ('mg', "MG"),
    ('micro_gram', "Micro Gram"),
    ('ml', "ml"),
    ('mmol', 'mmol'),
    ('drops', 'Drops'),
    ("iu", "IU"),
    ('u', "U"),
)


class VisitPrescription(AuShadhaBaseModel):

    """ Base Prescription Model for a OPD Visit """

    def __init__(self, *args, **kwargs):
        super(VisitPrescription, self).__init__(*args, **kwargs)
        self.__model_label__ = 'visit_prescription'
        self._parent_model = ['visit_detail']

    medicament = models.TextField(max_length=100, default='')
    indication = models.TextField(max_length=100,
                                  default='', blank=True, null=True)
    allow_substitution = models.BooleanField(default=False)
    print_prescription = models.BooleanField(default=False)
    dispensing_form = models.CharField(
        max_length=30,
        choices=DISPENSING_FORM_CHOICES,
        default='Tablet')
    route = models.CharField(
        max_length=30,
        default='Oral',
        choices=ROUTE_CHOICES)
    start_date = models.DateTimeField(
        'Treatment Start Date',
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True)
    end_date = models.DateTimeField('Treatment End Date', auto_now=False,
                                    auto_now_add=False, null=True, blank=True)
    treatment_duration = models.CharField(max_length=30, null=True, blank=True)
    dose = models.CharField(max_length=30)
    dose_unit = models.CharField(
        'Unit', max_length=30, choices=DOSE_UNIT_CHOICES)
    units = models.PositiveIntegerField(max_length=3,
                                        help_text="Quantity of medications to be given; \
                                  like number of tablets/ capsules")
    frequency = models.CharField(
        max_length=30,
        choices=ADMIN_FREQUENCY_CHOICES)
    admin_hours = models.TextField(
        max_length=250,
        default="",
        null=True,
        blank=True)
    review = models.DateTimeField(auto_now=False,
                                  auto_now_add=False,
                                  null=True, blank=True)
    refills = models.PositiveIntegerField(max_length=2, default=0)
    comment = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        default='')
    visit_detail = models.ForeignKey(
        'visit.VisitDetail', null=True, blank=True)

    class Meta:
        verbose_name = 'Visit Prescription'
        verbose_name_plural = 'Visit Prescription'
        ordering = ['print_prescription', 'allow_substitution',
                    'dispensing_form', 'medicament',
                    'indication', 'dose', 'dose_unit',
                    'frequency', 'admin_hours', 'route',
                    'start_date', 'end_date',
                    'treatment_duration',
                    'units', 'refills', 'comment']


# Eventually Replace text entries for fields above with auto suggestions from
# instance data below

class Units(models.Model):
    """ Stores the Units of Medicaments """
    pass


class Frequency(models.Model):
    """ Stores commonly entered Frequencies for a Medicament """
    pass


class AdminHours(models.Model):
    """ Stores commonly entered Administration Hours for Medicaments """
    pass


class DispensingForms(models.Model):
    """ Stores commonly dispensed Medication forms """
    pass


class Routes(models.Model):
    pass


# ModelForms

class VisitPrescriptionForm(AuShadhaBaseModelForm):

    dijit_fields = VISIT_PRESCRIPTION_FORM_CONSTANTS

    def __init__(self, *args, **kwargs):
        self.__form_name__ = "Visit Prescription Form"
        super(VisitPrescriptionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = VisitPrescription
        exclude = DEFAULT_VISIT_PRESCRIPTION_FORM_EXCLUDES
