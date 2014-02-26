################################################################################
# Project     : AuShadha
# Description : Views for Patient addition, editing, deleting, JSON export
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################



########################### General Module imports #############################

from datetime import datetime, date, time


########################### General Django Imports #############################

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


##################### Application Specific Model Imports #######################

import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic
from AuShadha.apps.ui.ui import ui as UI


######################## Import Models using UI.get_module() ###################

from .models import PatientDetail, PatientDetailForm
from dijit_widgets.tree import PatientTree

Demographics = UI.get_module('Demographics')
Contact = UI.get_module('Contact')
Phone = UI.get_module('Phone')
Guardian = UI.get_module('Guardian')
EmailAndFax = UI.get_module('EmailAndFax')

MedicalHistory = UI.get_module('MedicalHistory')
SurgicalHistory = UI.get_module('SurgicalHistory')
SocialHistory = UI.get_module('SocialHistory')
FamilyHistory = UI.get_module('FamilyHistory')
Immunisation = UI.get_module('Immunisation')

Allergy = UI.get_module('AllergyList')
MedicationList = UI.get_module("MedicationList")

AdmissionDetail = UI.get_module("Admission")

VisitDetail = UI.get_module("OPD_Visit")
VisitImaging = UI.get_module("OPD_Visit_Imaging")
VisitInv = UI.get_module("OPD_Visit_Inv")


############### THESE ARE OLD IMPORTS  ##########################################
 
 # With the new way of module import these are now obsolete. 
 # They are kept here purely in case something goes wrong.
 # Modules and Classes are now imported by the UI.get_module method
 # This loosely couples all modules and all the classes and allows developer to 
 # import modules interchangebly without causing ImportError
 
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
#from admission.models import AdmissionDetailForm
#from visit.models import VisitDetail, VisitImaging, VisitInv



#################### Import Utilities ##########################################

from .utilities import check_before_adding, return_patient_json





######################### Views start here ######################################


@login_required
def render_patient_json(request):

    if request.method =='GET':
      all_p = PatientDetail.objects.all()
      if all_p is not None:
          data = []
          for patient in all_p:
              print "Evaluating Patient: "
              print patient
              json = ModelInstanceJson(patient).return_data()
              data.append(json)
      else:
        data = {}
      json = simplejson.dumps(data)
      #print "\n"
      #print "-" *100
      #print "Printing Sample Patient JSON"
      #print "-" *100
      #print (simplejson.dumps(data[0]))
      #print "-" *100
      #print "\n"
      return HttpResponse(json, content_type="application/json")
    else:
      raise Http404("Bad Request Method")

@login_required
def render_patient_summary(request, patient_id=None):
    if request.method == "GET" and request.is_ajax():
        user = request.user

        if patient_id:
            patient_id = int(patient_id)
        else:
            patient_id = int(request.GET.get('patient_id'))

        try:
            pat_obj = PatientDetail.objects.get(pk=patient_id)
            var = ModelInstanceSummary(pat_obj).variable
            var['user']  = user
            variable = RequestContext(request, var)
            print "*" * 50
            print var
            print "*" * 50
            return render_to_response('patient_detail/summary.html', variable)

        except(AttributeError, NameError, KeyError, TypeError, ValueError):
            raise Http404("ERROR! Bad Request Parameters")

        except(AttributeError, NameError, KeyError, TypeError, ValueError):
            raise Http404("ERROR! Requested Patient Data Does not exist")
    else:
        raise Http404("Bad Request")

@login_required
def render_patient_info(request,patient_id = None):
  if request.user and request.method == 'GET':
    if patient_id:
      try:
        patient_id = int( patient_id )
        patient_detail_obj = PatientDetail.objects.get(pk = patient_id )
      except (NameError,ValueError,TypeError,AttributeError):
        raise Http404("Bad Request Parameters")
      except(PatientDetail.DoesNotExist):
        raise Http404("Requested Patient Does Not Exist")
      #data = {'success': True, 
              #'error_message': 'Successfully retrieved patient info',
              #'info': patient_detail_obj.__unicode__()
              #}
      #json = simplejson.dumps(data)
      #return HttpResponse(json, content_type='application/json')
      variable = RequestContext(request,
                                {'info': patient_detail_obj}
                                )
      return render_to_response( 'patient_detail/info.html', variable )
  else:
    return HttpResponseRedirect('login')


@login_required
def patient_detail_add(request, clinic_id = None):

    user = request.user
    print "Received a request to add a New Patient...."

    try:
      if clinic_id :
        clinic_id = int(clinic_id)
      else:
        clinic_id = int(request.GET.get('clinic_id'))
    except (KeyError,NameError,AttributeError,ValueError,TypeError):
        clinic_id = 1

    try:
      clinic = Clinic.objects.get(pk = clinic_id)          
      patient_detail_obj = PatientDetail(parent_clinic = clinic)
      if request.method == "GET" and request.is_ajax():
          patient_detail_form = PatientDetailForm(
              instance=patient_detail_obj)
          variable = RequestContext(request,
                                    {"user": user,
                                    "patient_detail_obj": patient_detail_obj,
                                    "patient_detail_form": patient_detail_form
                                    }
                                    )
          return render_to_response('patient_detail/add.html', variable)

      elif request.method == "POST"  and request.is_ajax():
          patient_detail_form = PatientDetailForm(request.POST,
                                                  instance = patient_detail_obj)
          if patient_detail_form.is_valid():
              saved_patient = patient_detail_form.save(commit = False)
              saved_patient.parent_clinic = clinic
              saved_patient.save()
              success = True
              error_message = "Patient Saved Successfully"
              form_errors = None
              #json = return_patient_json(saved_patient,success)
          else:
              form_errors = aumodelformerrorformatter_factory(patient_detail_form)
              saved_patient = None
              success = False
          data = {'success':success,
                  'error_message':form_errors,
                  'form_errors': form_errors
                  }
          json = simplejson.dumps(data)

      else:
          raise Http404('Bad Request:: Unsupported Request Method.')

    except(Clinic.DoesNotExist):
        saved_patient = None
        success = False
        data = {'success':success,'error_message':"No Clinic by the specified id"}
        json = simplejson.dumps(data)

    return HttpResponse(json, content_type='application/json')




@login_required
def patient_detail_edit(request, id):

    if request.user:
        user = request.user

        try:
            id = int(id)
            patient_detail_obj = PatientDetail.objects.get(pk=id)

            if not getattr(patient_detail_obj,'urls',None):
              patient_detail_obj.save()
              #print "*" * 100
              #print patient_detail_obj.urls['info']
              #print "*" * 100
        
        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")

        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient detail Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():

            patient_detail_edit_form = PatientDetailForm(auto_id = False, instance=patient_detail_obj)

            variable = RequestContext(request,
                                      {"user"   : user,
                                        "patient_detail_obj" : patient_detail_obj,
                                        "patient_detail_edit_form"   : patient_detail_edit_form
                                        }
                                      )

            return render_to_response('patient_detail/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            patient_detail_edit_form = PatientDetailForm(request.POST, instance=patient_detail_obj)

            if patient_detail_edit_form.is_valid():
                detail_object = patient_detail_edit_form.save()
                success = True
                error_message = "Patient Edited Successfully"
                form_errors = None
                #json = return_patient_json(detail_object, success=True)

            else:
                success = False
                error_message = "Error:: Patient Detail could not be edited."
                form_errors = ''
                for error in patient_detail_edit_form.errors:
                    form_errors += '<p>' + error + '</p>'
                #json = return_patient_json(detail_object=None, success=False)

            data  = {'success': success, 
                     'error_message': error_message, 
                     'form_errors': form_errors 
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_detail_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
            except TypeError or ValueError or AttributeError:
                if request.is_ajax():
                    success = False
                    error_message = '''
                            ERROR!! Bad Request. Please refresh page and try again.
                           '''
                    data = {"success": success, "error_message": error_message}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type="application/json")
                else:
                    raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                if request.is_ajax():
                    success = False
                    error_message = '''
                            ERROR!! Requested Patient Data Does not Exist.
                            Refresh Page and try again..
                           '''
                    data = {"success": success, "error_message": error_message}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type="application/json")
                else:
                    raise Http404(
                        "BadRequest: Patient detail Data Does Not Exist")
            if user.is_superuser:
                patient_detail_obj.delete()
                if request.is_ajax():
                    success = True
                    error_message = "Patient Deleted Successfully"
                    data = {"success": success, "error_message": error_message}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type="application/json")
                else:
                    return HttpResponseRedirect('/')
            else:
                if request.is_ajax():
                    success = False
                    error_message = "ERROR ! No Priviliges to Delete..."
                    data = {"success": success, "error_message": error_message}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type="application/json")
                else:
                    return HttpResponseRedirect('/')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")