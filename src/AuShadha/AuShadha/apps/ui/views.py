################################################################################
# Project     : AuShadha
# Description : Views for Initial UI Loading
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time
import importlib

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
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic

#from .models import PatientDetail, PatientDetailForm
#from demographics.demographics.models import Demographics
#from demographics.contact.models import Contact
#from demographics.phone.models import Phone
#from demographics.guardian.models import Guardian
#from demographics.email_and_fax.models import EmailAndFax
#from history.medical_history.models import MedicalHistory
#from history.surgical_history.models import SurgicalHistory
#from history.social_history.models import SocialHistory
#from history.family_history.models import FamilyHistory
#from history.obs_and_gyn.models import ObstetricHistoryDetail
#from immunisation.models import Immunisation
#from allergy_list.models import Allergy
#from medication_list.models import MedicationList
#from admission.models import AdmissionDetail, AdmissionDetailForm
#from visit.models import VisitDetail, VisitImaging, VisitInv



# Views start here -----------------------------------------


@login_required
def home(request):
  user = request.user

  if request.method == "GET":
    installed_apps =[]
    apps = settings.INSTALLED_APPS
    for app in apps:
      #Hack to avoid core modules. This way the UI atleast starts with core modules
      #as dependencies
      if not app.split('.')[0] == 'AuShadha':
        x = importlib.import_module(app)
        label = getattr(x,'MODULE_LABEL',None)
        print label
        if label:
          installed_apps.append(label)
        print x
    installed_apps = simplejson.dumps(installed_apps)
    variable = RequestContext(request, {'user':user,'installed_apps':installed_apps})
    print variable
    return render_to_response('ui/base.html',variable)

  else:
    raise Http404("Bad Request Method")