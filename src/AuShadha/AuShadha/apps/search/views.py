################################################################################
# Project     : AuShadha
# Description : Views for Search App
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################

""" 
  Holds the views for the Search application.
  This application will search Db for Patients 
  Can be configured to search for anything
"""

# General Module imports-----------------------------------
from datetime import datetime, date, time
import importlib
import json

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
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# AuShadha imports
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic

# Relative imports with UI.get_module()
PatientDetail = UI.get_module("PatientRegistration")
Demographics = UI.get_module("Demographics")
Contact = UI.get_module("Contact")
Phone = UI.get_module("Phone")
EmailAndFax = UI.get_module("EmailAndFax")
Guardian = UI.get_module("Guardian")


@login_required
def aushadha_patient_search(request, patient_id= None):
  '''
   Searches for Patients
  '''
  # FIXME Dojo sends REST queries with * suffix. This has to be split and dealt with before json generation is done.

  user = request.user

  if request.method == "GET" and request.is_ajax():
      if not patient_id:
          try:
              name = unicode(request.GET.get('name'))
              #print "You have queried Patients with Full Name containing: ", name
          except(TypeError, ValueError, NameError, KeyError):
              raise Http404(
                  "Bad Parameters.. No Search Results Could be returned. ")
          if name == "*":
              pat_obj = PatientDetail.objects.all()
          elif name[-1:] == "*":
              name = name[0:-1]
              #print "Name after stripping trailing '*' is: ", name
              pat_obj = PatientDetail.objects.filter(full_name__icontains=name)
          else:
              pat_obj = PatientDetail.objects.filter(full_name__icontains=name)
          jsondata = []

          if pat_obj:
              for patient in pat_obj:
                  data_to_append = {}
                  data_to_append['name'] = patient.full_name
                  data_to_append['id'] = patient.id
                  data_to_append['hospital_id'] = patient.patient_hospital_id
                  data_to_append['age'] = patient.age
                  data_to_append['sex'] = patient.sex
                  data_to_append['label'] = patient.full_name + "-" + \
                      patient.age       + "/" + \
                      patient.sex       + "(" + \
                      patient.patient_hospital_id + ")"
                  data_to_append['paneUrl'] = reverse('render_patient_pane_with_id', 
                                                      kwargs={'patient_id': patient.id}
                                                      )
                  jsondata.append(data_to_append)
          jsondump = json.dumps(jsondata)
          return HttpResponse(jsondump, content_type="application/json")

      elif patient_id:

          try:
            patient_id = int( patient_id )
            patient = PatientDetail.objects.get(pk= patient_id)
            jsondata = []
            if patient:
                data_to_append = {}
                data_to_append['name'] = patient.full_name
                data_to_append['id'] = patient.id
                data_to_append['hospital_id'] = patient.patient_hospital_id
                data_to_append['age'] = patient.age
                data_to_append['sex'] = patient.sex
                data_to_append['label'] = patient.full_name + "-" + \
                    patient.age       + "/" + \
                    patient.sex       + "(" + \
                    patient.patient_hospital_id + ")"
                data_to_append['paneUrl'] = reverse( 'render_patient_pane_with_id', 
                                                      kwargs={'patient_id': patient.id} 
                                                    )
                jsondata.append(data_to_append)
            jsondump = json.dumps(jsondata)
            return HttpResponse(jsondump, content_type="application/json")

          except(TypeError, KeyError, NameError, AttributeError):
              raise Http404("ERROR ! Bad Parameters. No Patients in result.")

          except(PatientDetail.DoesNotExist):
              raise Http404("ERROR! Patient Does Not Exist")

  else:
    raise Http404("Bad Request Method")


########################## OLD CODE. NEEDS TO BE RELOOKED. THIS WAS THE EARLY ADVANCED SEARCH IMPLEMENTATION #############

#@login_required
#def aushadha_advanced_patient_search(request, search_by, search_for):
    #if request.user:
        #user = request.user
        #search_by = request.GET['search_by']
        #search_for = request.GET['search_for']

        #if search_by == "first_name":
            #try:
                #patient_obj = PatientDetail.objects.filter(
                    #first_name__icontains=search_for)
                #variable = RequestContext(
                    #request, {'patient_obj': patient_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

        #elif search_by == "middle_name":
            #try:
                #patient_obj = PatientDetail.objects.filter(
                    #middle_name__icontains=search_for)
                #variable = RequestContext(
                    #request, {'patient_obj': patient_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

        #elif search_by == "last_name":
            #try:
                #patient_obj = PatientDetail.objects.filter(
                    #last_name__icontains=search_for)
                #variable = RequestContext(
                    #request, {'patient_obj': patient_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

        #elif search_by == "hospital_id":
            #try:
                #patient_obj = PatientDetail.objects.filter(
                    #patient_hospital_id__icontains=search_for)
                #variable = RequestContext(
                    #request, {'patient_obj': patient_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

        #elif search_by == "phone":
            #try:
                #phone_obj = Phone.objects.filter(
                    #phone__icontains=search_for)
                #variable = RequestContext(
                    #request, {'phone_obj': phone_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

        #elif search_by == "guardian_name":
            #try:
                #guardian_obj = Guardian.objects.filter(
                    #guardian_name__icontains=search_for)
                #variable = RequestContext(
                    #request, {'guardian_obj': guardian_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

        #elif search_by == "city":
            #try:
                #contact_obj = Contact.objects.filter(
                    #city__icontains=search_for)
                #variable = RequestContext(
                    #request, {'contact_obj': contact_obj, 'user': user})
                #return render_to_response('patient/patient_search_result.html', variable)
            #except ValueError or TypeError or AttributeError:
                #raise Http404("Please enter a correct search term")

    #else:
        #raise Http404("Please Log in")





#@login_required
#def patient_id_autocompleter(request, patient_id=None):
    #if request.method == "GET" and request.is_ajax():
        #request_copy = request.GET.copy()
        #if not patient_id:
            #patient_id = request_copy.get('patient_id')
        #else:
            #patient_id = int(patient_id)
        #patient_id_list = []
        #if patient_id != "*":
            #pat_obj = PatientDetail.objects.get(pk=patient_id)
            #if pat_obj:
                #dict_to_append = {}
                #dict_to_append[
                    #'patient_hospital_id'] = pat_obj.patient_hospital_id
                #dict_to_append['patient_id'] = pat_obj.id
                #dict_to_append['name'] = unicode(
                    #pat_obj.patient_hospital_id) + "-" + pat_obj.__unicode__()
                #dict_to_append['patient_name'] = pat_obj.__unicode__()
                #dict_to_append['first_name'] = pat_obj.first_name
                #dict_to_append['middle_name'] = pat_obj.middle_name
                #dict_to_append['last_name'] = pat_obj.last_name
                #dict_to_append['age'] = pat_obj.age
                #dict_to_append['sex'] = pat_obj.sex
                #patient_id_list.append(dict_to_append)
            #else:
                #dict_to_append = {"patient_name": "No-Result",
                                  #"name": "No Patients Recorded.",
                                  #"patient_id": "No-Result",
                                  #"patient_hospital_id": "",
                                  #"first_name": "",
                                  #"middle_name": "",
                                  #"last_name": "",
                                  #"age": "",
                                  #"sex": "",
                                  #}
                #patient_id_list.append(dict_to_append)
        #else:
            #dict_to_append = {"patient_name": "No-Result",
                              #"name": "No Patients Recorded.",
                              #"patient_id": "No-Result",
                              #"patient_hospital_id": "",
                              #"first_name": "",
                              #"middle_name": "",
                              #"last_name": "",
                              #"age": "",
                              #"sex": "",
                              #}
            #patient_id_list.append(dict_to_append)
        #jsondata = json.dumps(patient_id_list)
        #str_to_construct = json.dumps(patient_id_list)
        #f = open(
            #os.path.join(settings.CUSTOM_SCRIPT_ROOT, 'patient_id_list.json'), 'w')
        #f.write(str_to_construct)
        #f.close()
        #return HttpResponse(jsondata, content_type='application/json')
    #else:
        #raise Http404("Bad Request..")


#@login_required
#def hospital_id_autocompleter(request, patient_hospital_id=None):

    #if request.method == "GET" and request.is_ajax():
        #request_copy = request.GET.copy()

        #if not patient_hospital_id:
            #hospital_id = request_copy.get('patient_hospital_id')
        #else:
            #hospital_id = unicode(patient_hospital_id)

        #if hospital_id == "*":
            #pat_obj = PatientDetail.objects.all()
        #else:
            #if hospital_id[-1:] == "*":
                #hospital_id = hospital_id[:-1]
            #pat_obj = PatientDetail.objects.filter(
                #patient_hospital_id__startswith=hospital_id)
        #hospital_id_list = []

        #if pat_obj:
            #for pat in pat_obj:
                #dict_to_append = {}
                #dict_to_append['patient_hospital_id'] = pat.patient_hospital_id
                #dict_to_append['patient_id'] = pat.id
                #dict_to_append['name'] = unicode(
                    #pat.patient_hospital_id) + "-" + pat.__unicode__()
                #dict_to_append['patient_name'] = pat.__unicode__()
                #dict_to_append['first_name'] = pat.first_name
                #dict_to_append['middle_name'] = pat.middle_name
                #dict_to_append['last_name'] = pat.last_name
                #dict_to_append['age'] = pat.age
                #dict_to_append['sex'] = pat.sex
                #hospital_id_list.append(dict_to_append)
        #else:
            #dict_to_append = {"patient_name": "No-Result",
                              #"name": "No Patients Recorded.",
                              #"patient_id": "No-Result",
                              #"patient_hospital_id": "",
                              #"first_name": "",
                              #"middle_name": "",
                              #"last_name": "",
                              #"age": "",
                              #"sex": "",
                              #}
            #hospital_id_list.append(dict_to_append)
        #jsondata = json.dumps(hospital_id_list)

##    str_to_construct = "var PATIENT_LIST = " + str(hospital_id_list) +";"
        #str_to_construct = json.dumps(hospital_id_list)
        #f = open(
            #os.path.join(settings.CUSTOM_SCRIPT_ROOT, 'patient_list.json'), 'w')
        #f.write(str_to_construct)
        #f.close()
        #return HttpResponse(jsondata, content_type='application/json')
    #else:
        #raise Http404("Bad Request..")


#@login_required
#def patient_name_autocompleter(request, patient_name=None):

    #if request.method == "GET" and request.is_ajax():
        #request_copy = request.GET.copy()
        #patient_name_list = []
        #patient_id = None

        #if request.GET.get('patient_id'):
            #patient_id = int(request.GET.get('patient_id'))
        #if not patient_name:
            #patient_name = request_copy.get('patient_name')
        #else:
            #patient_name = unicode(patient_name)

        #if patient_name == "*":
            #pat_obj = PatientDetail.objects.all()
        #else:
            #if patient_name[-1:] == "*":
                #patient_name = patient_name[:-1]
            #if not patient_id:
                #pat_obj = PatientDetail.objects.filter(
                    #full_name__icontains=patient_name)
            #else:
                #pat_obj = PatientDetail.objects.filter(
                    #full_name__icontains=patient_name).filter(pk=patient_id)

        #if pat_obj:
            #for pat in pat_obj:
                #dict_to_append = {}
                #dict_to_append['patient_id'] = pat.id
                #dict_to_append['patient_hospital_id'] = pat.patient_hospital_id
                #dict_to_append['patient_name'] = pat.full_name
                #dict_to_append['first_name'] = pat.first_name
                #dict_to_append['middle_name'] = pat.middle_name
                #dict_to_append['last_name'] = pat.last_name
                #dict_to_append['age'] = pat.age
                #dict_to_append['sex'] = pat.sex
                #patient_name_list.append(dict_to_append)
        #else:
            #dict_to_append = {"patient_name": "No-Result",
                              #"name": "No Patients Recorded.",
                              #"patient_id": "No-Result",
                              #"patient_hospital_id": "",
                              #"first_name": "",
                              #"middle_name": "",
                              #"last_name": "",
                              #"age": "",
                              #"sex": "",
                              #}
            #patient_name_list.append(dict_to_append)
        #jsondata = json.dumps(patient_name_list)

        #str_to_construct = json.dumps(patient_name_list)
        #f = open(
            #os.path.join(settings.CUSTOM_SCRIPT_ROOT, 'patient_name_list.json'), 'w')
        #f.write(str_to_construct)
        #f.close()
        #return HttpResponse(jsondata, content_type='application/json')
    #else:
        #raise Http404("Bad Request..")

