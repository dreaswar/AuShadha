################################################################################
# Project: AuShadha
# Description: Pane of the UI for {{app_name}}
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
from django.template import Template, Context
from django.contrib.auth.decorators import login_required

from {{app_name}} import MODULE_LABEL
from {{app_name}}.models import *


@login_required
def render_{{app_name}}_pane(request, id = None):
  pass