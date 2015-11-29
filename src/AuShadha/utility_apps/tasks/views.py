##########################################################################
# Project     : AuShadha
# Description : Views for / tasks
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
##########################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.utils import simplejson
from django.core import serializers
#from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic


from .models import *
from dijit_widgets.tree import tasksTree


# Views start here -----------------------------------------


@login_required
def tasks_detail_list(request, id=None):
    pass


@login_required
def tasks_detail_add(request, id=None):
    pass


@login_required
def tasks_detail_edit(request, id):
    pass


@login_required
def tasks_detail_del(request, id):
    pass


def return_tasks_json(instance, success=True):
    json_obj = ModelInstanceJson(instance)
    return json_obj()


@login_required
def render_tasks_tree(request, id=None):
    pass


@login_required
def render_tasks_summary(request, id=None):
    pass


@login_required
def render_tasks_json(request, id=None):
    pass
