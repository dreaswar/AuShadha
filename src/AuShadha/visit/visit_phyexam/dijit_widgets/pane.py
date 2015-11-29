##########################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
##########################################################################

from cStringIO import StringIO
import yaml

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
import json
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.contrib.auth.decorators import login_required

from AuShadha.apps.ui.ui import UI

from patient import MODULE_LABEL
#from patient.models import PatientDetail
PatientDetail = UI.get_module("PatientRegistration")
VisitDetail = UI.get_module("OPD_Visit")
AdmissionDetail = UI.get_module("Admission")


@login_required
def render_phyexam_pane(request, visit_id=None):
    pass
