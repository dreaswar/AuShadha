# General Module imports-----------------------------------
from datetime import datetime, date, time
import yaml

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Template, Context

import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree


class VisitPrescriptionTree(object):

    """
     Defines the Dijit UI for Visit_prescription Tree
    """
    pass


def render_visit_prescription_tree(request, visit_detail_id=None):
    pass
