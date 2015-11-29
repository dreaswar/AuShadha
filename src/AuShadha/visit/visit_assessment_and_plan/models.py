##########################################################################
# Project      : AuShadha
# Description  : Models for AuShadha OPD Visits.
# Author       : Dr. Easwar TR
# Date         : 17-09-2013
# LICENSE      : GNU-GPL Version 3, Please see AuShadha/LICENSE.txt
##########################################################################

# General Imports
from datetime import datetime, date, time
import importlib


# Django Specific Imports
from django.db import models
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput

# Application model imports
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from AuShadha.apps.clinic.models import Clinic, Staff

from registry.inv_and_imaging.models import ImagingInvestigationRegistry, LabInvestigationRegistry
#from patient.models import PatientDetail
#from admission.models import AdmissionDetail

PatientDetail = UI.get_module("OPD_Visit")
#AdmissionDetail = UI.get_module("Admission")


from .dijit_fields_constants import VISIT_ASSESSMENT_AND_PLAN_FORM_CONSTANTS

DEFAULT_VISIT_DETAIL_FORM_EXCLUDES = ('visit_detail',)


class VisitAssessmentAndPlan(AuShadhaBaseModel):

    """Model to describe the Visit Assessment and Plan"""

    def __init__(self, *args, **kwargs):
        super(VisitAssessmentAndPlan, self).__init__(*args, **kwargs)
        self.__model_label__ = "visit_assessment_and_plan"
        self._parent_model = 'visit_detail'

    case_summary = models.TextField(
        "Case Summary & Assessment",
        max_length=1000,
        help_text="Restrict to 1000 words. \nSummarise the case and your assessment")

    possible_diagnosis = models.TextField(
        "Possible Diagnosis",
        max_length=1000,
        help_text="Restrict to 1000 words\nPlease enter in separate lines")

    plan = models.TextField(
        "Plan",
        max_length=1000,
        help_text="Restrict to 1000 words\nPlease enter in separate lines")

    visit_detail = models.ForeignKey('visit.VisitDetail')

    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)

    def __unicode__(self):
        return '%s\n%s\n%s\n%s\nSeen On: %s' % (
            self.case_summary,
            self.possible_diagnosis,
            self.plan,
            self.visit_detail,
            self.visit_detail.visit_date.date().isoformat()
        )


class VisitAssessmentAndPlanForm(AuShadhaBaseModelForm):

    __form_name__ = "Visit Assessment & Plan Form"

    dijit_fields = VISIT_ASSESSMENT_AND_PLAN_FORM_CONSTANTS

    class Meta:
        model = VisitAssessmentAndPlan
        exclude = ('visit_detail', 'parent_clinic', 'created_at')
