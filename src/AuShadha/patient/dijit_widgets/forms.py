################################################################################
# Project: AuShadha
# Description: Forms for Patient
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

from cStringIO import StringIO
import yaml

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
import json
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm

from patient import MODULE_LABEL
from patient.models import PatientDetail
from patient.dijit_fields_constants import PATIENT_DETAIL_FORM_CONSTANTS

form_template = open('patient/dijit_widgets/form.yaml', 'r' )

patient_detail_form_fields = yaml.load(form_template.read() )['PATIENT_DETAIL_FORM']

form_template.close()

class PatientDetailForm(AuShadhaBaseModelForm):

    """
        ModelForm for Patient Basic Data
    """

    __form_name__ = "Patient Detail Form"

    dijit_fields = patient_detail_form_fields
    print dijit_fields
    #print type(PATIENT_DETAIL_FORM_CONSTANTS)
    #print PATIENT_DETAIL_FORM_CONSTANTS
    #print "*" * 100
    #print patient_detail_form_fields
    #print "*" * 100
    #print patient_detail_form_fields == PATIENT_DETAIL_FORM_CONSTANTS
    #dijit_fields = PATIENT_DETAIL_FORM_CONSTANTS

    class Meta:
        model = PatientDetail
        exclude = ('parent_clinic', )