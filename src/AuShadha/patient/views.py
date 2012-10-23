##--------------------------------------------------------------
# Views for Patient contact and details display and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date: 26-09-2010
##---------------------------------------------------------------

#import wx
import os, sys

# General Django Imports----------------------------------

from django.shortcuts                import render_to_response
from django.http                     import Http404, HttpResponse, HttpResponseRedirect
from django.template                 import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models      import User


from django.views.decorators.csrf   import csrf_exempt
from django.views.decorators.cache  import never_cache
from django.views.decorators.csrf   import csrf_protect
from django.views.decorators.debug  import sensitive_post_parameters

from django.core.paginator           import Paginator

from django.utils                    import simplejson
from django.core                     import serializers
from django.core.serializers         import json    
from django.core.serializers.json    import DjangoJSONEncoder

from django.contrib.auth.views       import login, logout
from django.contrib.auth.decorators  import login_required
from django.contrib.auth             import REDIRECT_FIELD_NAME
from django.contrib.auth.forms       import AuthenticationForm
from django.template.response        import TemplateResponse
from django.contrib.sites.models     import get_current_site
import urlparse

# General Module imports-----------------------------------
from datetime import datetime, date, time



# Application Specific Model Imports-----------------------
from patient.models   import *
from admission.models import *
#from discharge.models import *
#from visit.models     import *

import AuShadha.settings as settings

from patient.medication_list import patient_medication_list_add, patient_medication_list_edit
from patient.immunisation import patient_immunisation_add, patient_immunisation_edit
from patient.family_history import patient_family_history_add, patient_family_history_edit

#Views start here -----------------------------------------



################################################################################

def generate_json_for_datagrid(obj, success=True, error_message = "Saved Successfully", form_errors  = None):
    """
      Returns the JSON formatted Values of a specific Django Model Instance for use with Dojo Grid.
      A few default DOJO Grid Values are specified, rest are instance specific and are generated on the fly.
      It assumes the presence of get_edit_url and get_del_url in the model instances passed to it via obj.

      ARGUMENTS: obj           : model instace / queryset
                 success       : A success message 
                 error_message : Error Message if any.
                 form_errors   : Form Validation Errors from Django while saving can be passed.
    """
    print "TRYING TO RETURN JSON FOR OBJECT: ", obj
    json_data = []

    try:
      iterable = iter(obj)
      if iterable:
        for element in obj:
          print element._meta.fields
          print "APP LABEL IS", element._meta.app_label
          data = { 'success'       : success, 
                   'error_message' : unicode(error_message) ,
                   'form_errors'   : form_errors,
                   'edit'          : getattr(element, 'get_edit_url()',element.get_edit_url()),
                   'del'           : getattr(element, 'get_del_url()',element.get_del_url()),
                   'patient_detail': getattr(element, 'patient_detail.__unicode__()', None)
                 }
          for i in element._meta.fields:
            print "CURRENT ITERATING FIELD NAME IS : ", i
            print "DATA DICTIONARY NOW IS ", data.keys()
            if i.name not in data.keys():
              print "Adding ", i.name
              print i.name.__class__
              try:
                if i.name == 'aushadhabasemodel_ptr':
                  data[i.name] = "AuShadhaBaseModel"
                else:
                  data[i.name] = getattr(element, i.name, None)
              except(TypeError):
                raise Exception("Error In serialization..")
          json_data.append(data)

    except TypeError:
      print obj._meta.fields
      data = { 'success'       : success, 
               'error_message' : unicode(error_message) ,
               'form_errors'   : form_errors,
               'edit'          : getattr(obj, 'get_edit_url()',obj.get_edit_url()),
               'del'           : getattr(obj, 'get_del_url()',obj.get_del_url()),
               'patient_detail': getattr(obj, 'patient_detail.__unicode__()', None)
             }
      for i in obj._meta.fields:
        print "CURRENT ITERATING FIELD NAME IS : ", i
        print "DATA DICTIONARY NOW IS ", data.keys()
        if i.name not in data.keys():
          print "Adding ", i.name
          print i.name.__class__
          try:
            if i.name == 'aushadhabasemodel_ptr':
              data[i.name] = "AuShadhaBaseModel"
            else:
              data[i.name] = getattr(obj, i.name, None)
          except(TypeError):
            raise Exception("Error In serialization..")
      json_data.append(data)
    
#    json_serializer = serializers.get_serializer('json')()
#    json_data = json_serializer.serialize(json_data, ensure_ascii = False)    
    json_data = simplejson.dumps(json_data, cls=DjangoJSONEncoder)
#    json_data = simplejson.dumps(json_data)
    print "RETURNED JSON IS ", unicode(json_data)
    return json_data


def return_patient_json(patient, success = True):
    data ={"addData":{}}
    if patient:
        data_to_append = data['addData']
        data_to_append['id']                   = patient.id
        data_to_append['patient_hospital_id']  = patient.patient_hospital_id

        data_to_append['full_name']          = patient.full_name
        data_to_append['first_name']           = patient.first_name
        data_to_append['middle_name']          = patient.middle_name
        data_to_append['last_name']            = patient.last_name
        data_to_append['age']                  = patient.age
        data_to_append['sex']                  = patient.sex

        data_to_append['home']         = patient.get_patient_main_window_url()
        data_to_append['edit']         = patient.get_patient_detail_edit_url()
        data_to_append['del']          = patient.get_patient_detail_del_url()

        data_to_append['contactadd']   = patient.get_patient_contact_add_url()
        data_to_append['contactlist']  = patient.get_patient_contact_list_url()

        data_to_append['phoneadd']     = patient.get_patient_phone_add_url()
        data_to_append['phonelist']    = patient.get_patient_phone_list_url()
        data_to_append['guardianadd']  = patient.get_patient_guardian_add_url()
        data_to_append['guardianlist'] = patient.get_patient_guardian_list_url()
        data_to_append['emailadd']     = patient.get_patient_email_and_fax_add_url()
        data_to_append['emaillist']    = patient.get_patient_email_and_fax_list_url()

        data_to_append['admissionadd']  = patient.get_patient_admission_add_url()
        data_to_append['visitadd']      = patient.get_patient_visit_add_url()
        data_to_append['admissionlist'] = patient.get_patient_admission_list_url()
        data_to_append['visitlist']     = patient.get_patient_visit_list_url()
    if success:
      error_message           = "Patient Detail Saved Successfully"
      form_errors             = None
    else:
      success                 = False
      error_message           = "Error! Form could not be saved. "
      form_errors             = True
    data['success']       = success
    data['error_message'] = error_message
    data['form_errors']   = form_errors
    json = simplejson.dumps(data)
    print "JSON=", json
    return json

####################################################################################


def check_before_adding(patient_obj):
    patient_object    = patient_obj
    patient_id        = patient_object.patient_hospital_id
    all_patients      = PatientDetail.objects.all()
    active_admissions = Admission.objects.filter(patient_detail = patient_object).filter(admission_closed = 'False')
    active_visit      = patient_object.has_active_visit()
    id_list           = []
    for patient in all_patients:
        id_list.append(patient.patient_hospital_id)
    if patient_id in id_list:
        error = "This ID is already Taken. Please renter and retry"
        print error
        return False
    else:
        if active_visit == False:
            if active_admissions == False:
                print 'All checked.. Everything ok.. '
                return True
            else:
                error = 'This patient has active admissions. Please discharge and retry.'
                print error
                return False
        else:
            error = "This patient has active visit. Please discharge and retry."
            print error
            return False

######################################################################################


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_view(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            data  = {'success'       : True, 
                     'error_message' : "Successfully Loggged In !", 
                     'redirect_to'   : redirect_to
                    }
        else:
           data  = {'success'       : False, 
                     'error_message' : '''<em class='error_text'>ERROR! Could not login</em>
                                         <p class='suggestion_text'>Please Check your Username & Password.</p>
                                         <i class='help_text'>If you are sure they are correct, 
                                         Please contact Administrator to find 
                                         out whether you need to activate your account.
                                         </i>
                                       ''',
                  }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type = 'application/json')
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def logout_view(request):
    '''
    View for logging out of AuShadha
    '''
    logout(request)
    return HttpResponseRedirect('/AuShadha/')
#    return HttpResponseRedirect('/login/')


@login_required
def patient_index(request):
    '''
    View for Generating Patient List

    Takes on Request Object as argument.
    '''
    user = request.user
    all_patients = PatientDetail.objects.all().order_by('patient_hospital_id')
    variable = RequestContext(request, {"all_patients"  :  all_patients  ,'user'   :   user  })
    return render_to_response('patient/index.html', variable)


@login_required
def patient_id_autocompleter(request, patient_id = None):
  if request.method == "GET" and request.is_ajax():
    request_copy  = request.GET.copy();
    if not patient_id:
      patient_id   = request_copy.get('patient_id')
    else:
      patient_id = int(patient_id)
    print patient_id
    patient_id_list = []
    if patient_id  != "*":
      pat_obj  = PatientDetail.objects.get(pk = patient_id)
      print pat_obj
      if pat_obj:
          dict_to_append   = {}
          dict_to_append['patient_hospital_id'] = pat_obj.patient_hospital_id
          dict_to_append['patient_id']          = pat_obj.id
          dict_to_append['name']                = unicode(pat_obj.patient_hospital_id) + "-" + pat_obj.__unicode__()
          dict_to_append['patient_name']        = pat_obj.__unicode__()
          dict_to_append['first_name']          = pat_obj.first_name
          dict_to_append['middle_name']         = pat_obj.middle_name
          dict_to_append['last_name']           = pat_obj.last_name
          dict_to_append['age']                 = pat_obj.age
          dict_to_append['sex']                 = pat_obj.sex
          patient_id_list.append(dict_to_append)
      else:
        dict_to_append = {"patient_name": "No-Result", 
                          "name"        : "No Patients Recorded.",
                          "patient_id"  : "No-Result",
                          "patient_hospital_id":"",
                          "first_name"  : "",
                          "middle_name" : "",
                          "last_name"   : "",
                          "age"         : "",
                          "sex"         : "",
                       }
        patient_id_list.append(dict_to_append)
    else:
      dict_to_append = {"patient_name": "No-Result", 
                        "name"        : "No Patients Recorded.",
                        "patient_id"  : "No-Result",
                        "patient_hospital_id":"",
                        "first_name"   : "",
                        "middle_name"  : "",
                        "last_name"    :  "",
                        "age"          : "",
                        "sex"          : "",
                       }
      patient_id_list.append(dict_to_append)
    json = simplejson.dumps(patient_id_list)
    print json
    str_to_construct = simplejson.dumps(patient_id_list) 
    f = open( os.path.join(settings.CUSTOM_SCRIPT_ROOT, 'patient_id_list.json') , 'w')
    f.write(str_to_construct)
    f.close()
    return HttpResponse(json, content_type ='application/json')
  else:
    raise Http404("Bad Request..")


@login_required
def hospital_id_autocompleter(request, patient_hospital_id = None):
  if request.method == "GET" and request.is_ajax():
    request_copy  = request.GET.copy();
    if not patient_hospital_id:
      hospital_id   = request_copy.get('patient_hospital_id')
    else:
      hospital_id = unicode(patient_hospital_id)
    print hospital_id
    if hospital_id  == "*":
      pat_obj = PatientDetail.objects.all()
    else:
      if hospital_id[-1:] == "*":
        hospital_id = hospital_id[:-1]
      pat_obj  = PatientDetail.objects.filter(patient_hospital_id__startswith = hospital_id)
    print pat_obj
    hospital_id_list = []
    if pat_obj:
      for pat in pat_obj:
        dict_to_append   = {}
        dict_to_append['patient_hospital_id'] = pat.patient_hospital_id
        dict_to_append['patient_id']          = pat.id
        dict_to_append['name']                = unicode(pat.patient_hospital_id) + "-" + pat.__unicode__()
        dict_to_append['patient_name']        = pat.__unicode__()
        dict_to_append['first_name']          = pat.first_name
        dict_to_append['middle_name']         = pat.middle_name
        dict_to_append['last_name']           = pat.last_name
        dict_to_append['age']                 = pat.age
        dict_to_append['sex']                 = pat.sex
        hospital_id_list.append(dict_to_append)
    else:
      dict_to_append = {"patient_name": "No-Result", 
                        "name"        : "No Patients Recorded.",
                        "patient_id"  : "No-Result",
                        "patient_hospital_id":"",
                        "first_name" : "",
                        "middle_name": "",
                        "last_name"  : "",
                        "age"        : "",
                        "sex"        : "",
                       }
      hospital_id_list.append(dict_to_append)
    json = simplejson.dumps(hospital_id_list)
    print json
#    str_to_construct = "var PATIENT_LIST = " + str(hospital_id_list) +";"
    str_to_construct = simplejson.dumps(hospital_id_list) 
    f = open( os.path.join(settings.CUSTOM_SCRIPT_ROOT, 'patient_list.json') , 'w')
    f.write(str_to_construct)
    f.close()
    return HttpResponse(json, content_type ='application/json')
  else:
    raise Http404("Bad Request..")

@login_required
def patient_name_autocompleter(request, patient_name = None):
  if request.method == "GET" and request.is_ajax():
    request_copy  = request.GET.copy();
    patient_name_list = []
    patient_id = None
    if request.GET.get('patient_id'):
      patient_id = int(request.GET.get('patient_id'))
    if not patient_name:
      patient_name   = request_copy.get('patient_name')
    else:
      patient_name = unicode(patient_name)
    print patient_name
    if patient_name  == "*":
      pat_obj = PatientDetail.objects.all()
    else:
      if patient_name[-1:] == "*":
        patient_name = patient_name[:-1]
      if not patient_id:
        pat_obj  = PatientDetail.objects.filter(full_name__icontains = patient_name)
      else:
        pat_obj  = PatientDetail.objects.filter(full_name__icontains = patient_name).filter(pk = patient_id)
    print pat_obj
    if pat_obj:
      for pat in pat_obj:
        dict_to_append                        = {}
        dict_to_append['patient_id']          = pat.id
        dict_to_append['patient_hospital_id'] = pat.patient_hospital_id
        dict_to_append['patient_name']        = pat.full_name
        dict_to_append['first_name']          = pat.first_name
        dict_to_append['middle_name']         = pat.middle_name
        dict_to_append['last_name']           = pat.last_name
        dict_to_append['age']                 = pat.age
        dict_to_append['sex']                 = pat.sex
        patient_name_list.append(dict_to_append)
    else:
      dict_to_append = {"patient_name": "No-Result", 
                        "name"        : "No Patients Recorded.",
                        "patient_id"  : "No-Result",
                        "patient_hospital_id":"",
                        "first_name" : "",
                        "middle_name": "",
                        "last_name"  : "",
                        "age"        : "",
                        "sex"        : "",
                       }
      patient_name_list.append(dict_to_append)
    json = simplejson.dumps(patient_name_list)
    print json
    str_to_construct = simplejson.dumps(patient_name_list) 
    f = open( os.path.join(settings.CUSTOM_SCRIPT_ROOT, 'patient_name_list.json') , 'w')
    f.write(str_to_construct)
    f.close()
    return HttpResponse(json, content_type ='application/json')
  else:
    raise Http404("Bad Request..")


######################################################################################

@login_required
def patient_list(request):
    '''
    View for Generating Patient List
    Takes on Request Object as argument.
    '''
    user = request.user
    all_patients = PatientDetail.objects.all().order_by('first_name')
    variable            = RequestContext(request,{'user'         : user,
                                                  "all_patients" : all_patients  
                                                 })
    return render_to_response('patient/patient_list.html', variable)

@login_required
def alternate_layout(request):
    '''

    View for Generating an alternate layout for sandboxing purposes...
    '''
    user = request.user
    all_patients = PatientDetail.objects.all().order_by('first_name')
    variable            = RequestContext(request,{'user'         : user,
                                                  "all_patients" : all_patients  
                                                 })
    return render_to_response('base_alternate.html', variable)


@login_required
def render_patient_list(request):
  '''
    View for Generating Patient List
    Takes on Request Object as argument.
  '''
  user = request.user
  data         = []
  print request.GET
  keys = ["sort( first_name)", "sort(-first_name)","sort(+first_name)",
          "sort( last_name)", "sort(-last_name)", "sort(+last_name)",
          "sort( age)", "sort(-age)", "sort(+sex)",
          "sort( sex)", "sort(-sex)", "sort(+age)",
          "sort( patient_hospital_id)", "sort(-patient_hospital_id)", 
          "sort(+patient_hospital_id)"
          ]
  key_sort_map = {
  "sort(+patient_hospital_id)": "patient_hospital_id",
  "sort( patient_hospital_id)": "patient_hospital_id",
  "sort(-patient_hospital_id)": "-patient_hospital_id",
  "sort(+first_name)": "first_name",
  "sort( first_name)": "first_name",
  "sort(-first_name)": "-first_name",
  "sort(+last_name)" : "last_name",
  "sort( last_name)" : "last_name",
  "sort(-last_name)" : "-last_name",
  "sort(+sex)"       : "sex",
  "sort( sex)"       : "sex",
  "sort(-sex)"       : "-sex",
  "sort(+age)"       : "age",
  "sort( age)"       : "age",
  "sort(-age)"       : "-age",
  }

  search_field_list = ['id', 
                  'patient_hospital_id',
                  'full_name' ,
                  'first_name' ,
                  'middle_name',
                  'last_name'  ,
                  'age','sex',
                  'patient_id'
                 ]

  get_query_item_map = { 'id':"pk", 
                         'full_name' : 'full_name',
                         'first_name':"first_name",
                         'middle_name':"middle_name",
                         'last_name':"last_name",
                         'patient_hospital_id':"patient_hospital_id",
                         'age':"age",
                         'sex':"sex",
                         'patient_id':"pk"
                       }

  def create_patient_list_json(all_patients):
    for patient in all_patients:
      data_to_append = {}
      data_to_append['id']                   = patient.id
      data_to_append['patient_hospital_id']  = patient.patient_hospital_id
      data_to_append['full_name']           = patient.full_name
      data_to_append['first_name']           = patient.first_name
      data_to_append['middle_name']          = patient.middle_name
      data_to_append['last_name']            = patient.last_name
      data_to_append['age']                  = patient.age
      data_to_append['sex']                  = patient.sex

      data_to_append['home']         = patient.get_patient_main_window_url()
      data_to_append['edit']         = patient.get_patient_detail_edit_url()
      data_to_append['del']          = patient.get_patient_detail_del_url()

      data_to_append['contactadd']   = patient.get_patient_contact_add_url()
      data_to_append['contactlist']  = patient.get_patient_contact_list_url()
      data_to_append['phoneadd']     = patient.get_patient_phone_add_url()
      data_to_append['phonelist']    = patient.get_patient_phone_list_url()
      data_to_append['guardianadd']  = patient.get_patient_guardian_add_url()
      data_to_append['guardianlist'] = patient.get_patient_guardian_list_url()
      data_to_append['emailadd']     = patient.get_patient_email_and_fax_add_url()
      data_to_append['emaillist']    = patient.get_patient_email_and_fax_list_url()

      data_to_append['admissionadd']  = patient.get_patient_admission_add_url()
      data_to_append['visitadd']      = patient.get_patient_visit_add_url()
      data_to_append['admissionlist'] = patient.get_patient_admission_list_url()
      data_to_append['visitlist']     = patient.get_patient_visit_list_url()

      data.append(data_to_append)
    json = simplejson.dumps(data)
    print json
    return HttpResponse(json, content_type = "application/json")

  if request.GET.get('search_field') in search_field_list and \
     request.GET.get('search_for'):

    search_field = unicode(request.GET.get('search_field'))
    search_for   = unicode(request.GET.get('search_for'))
    search_query_map = {
      "id" : PatientDetail.objects.all(),
      "full_name" : PatientDetail.objects.filter(full_name__icontains = search_for).order_by('first_name'),
      "first_name" : PatientDetail.objects.filter(first_name__startswith = search_for),
      "middle_name" : PatientDetail.objects.filter(middle_name__startswith = search_for),
      "last_name" : PatientDetail.objects.filter(last_name__startswith = search_for),
      "age"                : PatientDetail.objects.filter(age__startswith = search_for),
      "sex" : PatientDetail.objects.filter(sex__startswith = search_for),
      "patient_hospital_id" : PatientDetail.objects.filter(patient_hospital_id__startswith = search_for),
    }

    if search_field != "id":

      if search_for == "*":
        print "Searching for ", search_field, " in All patients "
        all_patients = PatientDetail.objects.all()
      elif search_for[-1:] == "*":
        search_for = search_for[0:-1]
        print "Searching for ", search_field, \
               " in patients filtered for", search_for
        all_patients = search_query_map[search_field]
      else:
        print "Searching for ", search_field, \
               " in patients filtered for", search_for
        all_patients = search_query_map[search_field]
      return create_patient_list_json(all_patients)

    elif search_field == "id":
      if search_for == "*":
        print "Searching for ID in All Patients"
        all_patients = PatientDetail.objects.all()
        return create_patient_list_json(all_patients)
      elif search_for[-1:] == "*":
        print "Searching for ID in Patients starting with ", search_for[0:-1]
        search_for   = int(search_for[0:-1])
        all_patients = search_query_map[search_field]
        return create_patient_list_json(all_patients)
      else:
        try:
          search_for = int(search_for)
          pat_obj = PatientDetail.objects.get(pk = search_for)
          print "RETURNING PATIENT WITH ID: ", search_for , "--", pat_obj
          json = return_patient_json(pat_obj)
          return HttpResponse(json, content_type = "application/json")
        except(ValueError, TypeError, NameError, KeyError, AttributeError):
          raise Http404("ERROR! Invalid request Parameters")
        except(PatientDetail.DoesNotExist):
          raise Http404("ERROR! No Patient Data Found. ")

  else:
       raise Http404("ERROR! Invalid Search parameters")


################################################################################

@login_required
def contact_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id	                    = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_contact_add(request, id)
    patient_detail_obj			= PatientDetail.objects.get(pk = id)
  except(AttributeError, NameError, TypeError, ValueError, KeyError):
    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")
  patient_contact_obj			= PatientContact.objects.filter(patient_detail = patient_detail_obj)
  json = generate_json_for_datagrid(patient_contact_obj)
  print json
  return HttpResponse(json, content_type = "application/json")



@login_required
def phone_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id	                    = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_phone_add(request, id)
    patient_detail_obj			= PatientDetail.objects.get(pk = id)
  except(AttributeError, NameError, TypeError, ValueError, KeyError):
    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")
  patient_phone_obj			= PatientPhone.objects.filter(patient_detail = patient_detail_obj)
  json = generate_json_for_datagrid(patient_phone_obj)
  return HttpResponse(json, content_type = "application/json")


@login_required
def guardian_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id	                    = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_guardian_add(request, id)
    patient_detail_obj			= PatientDetail.objects.get(pk = id)
  except(AttributeError, NameError, TypeError, ValueError, KeyError):
    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")
  patient_guardian_obj			= PatientGuardian.objects.filter(patient_detail = patient_detail_obj)
  json = generate_json_for_datagrid(patient_guardian_obj)
  return HttpResponse(json, content_type = "application/json")


@login_required
def demographics_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id                      = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_demographics_add(request, id)
    patient_detail_obj         = PatientDetail.objects.get(pk = id)
    patient_demographics_obj   = PatientDemographicsData.objects.filter(patient_detail = patient_detail_obj)
    json = generate_json_for_datagrid(patient_demographics_obj)
    return HttpResponse(json, content_type = "application/json")
#  except(AttributeError, NameError, TypeError, ValueError, KeyError):
#    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")

@login_required
def allergies_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id                      = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_allergies_add(request, id)
    patient_detail_obj      = PatientDetail.objects.get(pk = id)
    patient_allergies_obj   = PatientAllergies.objects.filter(patient_detail = patient_detail_obj)
#    json_list = []
#    for allergy in patient_allergies_obj:
#      json = allergy.generate_json_for_datagrid()
#      json_list.append(json)
#    print "ALLERGIES JSON LIST TO BE RETURNED BY THE VIEW IS: ", json_list
#    json_list = simplejson.dumps(json_list)
    json = generate_json_for_datagrid(patient_allergies_obj)
    return HttpResponse(json, content_type = "application/json")
#  except(AttributeError, NameError, TypeError, ValueError, KeyError):
#    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")

@login_required
def immunisation_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id                      = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_immunisation_add(request, id)
    patient_detail_obj      = PatientDetail.objects.get(pk = id)
    patient_immunisation_obj   = PatientImmunisation.objects.filter(patient_detail = patient_detail_obj)
#    json_list = []
#    for immunisation in patient_immunisation_obj:
#      json = immunisation.generate_json_for_datagrid()
#      json_list.append(json)
#    print "ALLERGIES JSON LIST TO BE RETURNED BY THE VIEW IS: ", json_list
#    json_list = simplejson.dumps(json_list)
    json = generate_json_for_datagrid(patient_immunisation_obj)
    return HttpResponse(json, content_type = "application/json")
#  except(AttributeError, NameError, TypeError, ValueError, KeyError):
#    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")

@login_required
def family_history_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id                      = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_family_history_add(request, id)
    patient_detail_obj      = PatientDetail.objects.get(pk = id)
    patient_family_history_obj   = PatientFamilyHistory.objects.filter(patient_detail = patient_detail_obj)
#    json_list = []
#    for family_history in patient_family_history_obj:
#      json = family_history.generate_json_for_datagrid()
#      json_list.append(json)
#    print "ALLERGIES JSON LIST TO BE RETURNED BY THE VIEW IS: ", json_list
#    json_list = simplejson.dumps(json_list)
    json = generate_json_for_datagrid(patient_family_history_obj)
    return HttpResponse(json, content_type = "application/json")
#  except(AttributeError, NameError, TypeError, ValueError, KeyError):
#    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")

@login_required
def medication_list_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id                      = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_medication_list_add(request, id)
    patient_detail_obj      = PatientDetail.objects.get(pk = id)
    patient_medication_list_obj   = PatientMedicationList.objects.filter(patient_detail = patient_detail_obj)
#    json_list = []
#    for medication_list in patient_medication_list_obj:
#      json = medication_list.generate_json_for_datagrid()
#      json_list.append(json)
#    print "ALLERGIES JSON LIST TO BE RETURNED BY THE VIEW IS: ", json_list
#    json_list = simplejson.dumps(json_list)
    json = generate_json_for_datagrid(patient_medication_list_obj)
    return HttpResponse(json, content_type = "application/json")
#  except(AttributeError, NameError, TypeError, ValueError, KeyError):
#    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def admission_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id	                    = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_admission_add(request, id)
    patient_detail_obj			= PatientDetail.objects.get(pk = id)
  except(AttributeError, NameError, TypeError, ValueError, KeyError):
    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")
  patient_admission_obj			= Admission.objects.filter(patient_detail = patient_detail_obj)
  data                    = []
  if patient_admission_obj:
    for admission in patient_admission_obj:
      data_to_append = {}
      data_to_append['id']                   = admission.id
      data_to_append['date_of_admission']    = admission.date_of_admission.isoformat()
      data_to_append['time_of_admission']    = admission.time_of_admission.isoformat()
      data_to_append['admitting_surgeon']    = admission.admitting_surgeon.surgeon_name
      data_to_append['room_or_ward']         = admission.room_or_ward
      data_to_append['admission_closed']     = admission.admission_closed
      data_to_append['hospital']             = admission.hospital
      data_to_append['home']                 = admission.get_admission_main_window_url()
      data_to_append['edit']                 = admission.get_admission_edit_url()
      data_to_append['del']                  = admission.get_admission_del_url()
      data.append(data_to_append)
  json   = simplejson.dumps(data)
  return HttpResponse(json, content_type = "application/json")


@login_required
def visit_json(request):
  try:
    action                  = unicode(request.GET.get('action'))
    id	                    = int(request.GET.get('patient_id'))
    if action == 'add':
      return patient_visit_add(request, id)
    patient_detail_obj			= PatientDetail.objects.get(pk = id)
  except(AttributeError, NameError, TypeError, ValueError, KeyError):
    raise Http404("ERROR:: Bad request.Invalid arguments passed")
  except(PatientDetail.DoesNotExist):
    raise Http404("ERROR:: Patient requested does not exist.")
  patient_visit_obj			= VisitDetail.objects.filter(patient_detail = patient_detail_obj)
  data                    = []
  if patient_visit_obj:
    for visit in patient_visit_obj:
      data_to_append = {}
      data_to_append['id']               = visit.id
      data_to_append['visit_date']       = visit.visit_date
      data_to_append['op_surgeon']       = visit.op_surgeon
      data_to_append['is_active']        = visit.is_active
      data_to_append['referring_doctor'] = visit.referring_doctor
      data_to_append['consult_nature']   = visit.consult_nature
      data_to_append['remarks']          = visit.remarks
      data_to_append['edit']             = visit.get_patient_visit_edit_url()
      data_to_append['del']              = visit.get_patient_visit_del_url()
      data.append(data_to_append)
  json   = simplejson.dumps(data)
  return HttpResponse(json, content_type = "application/json")



########################################################################################################


@login_required
def patient_allergies_add(request,id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_allergies_obj       = PatientAllergies(patient_detail = patient_detail_obj)
        patient_allergies_add_form  = PatientAllergiesForm(instance = patient_allergies_obj)
        variable                = RequestContext(request, 
        																					{"user" 									:	user,
        																					 "patient_detail_obj"			:	patient_detail_obj ,
        																					 "patient_allergies_add_form" :	patient_allergies_add_form, 
																									 "patient_allergies_obj" 		  :	patient_allergies_obj ,
																									})
#      except TypeError or ValueError or AttributeError:
#        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/allergies/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_allergies_obj       = PatientAllergies(patient_detail = patient_detail_obj)
        patient_allergies_add_form  = PatientAllergiesForm(request.POST,instance = patient_allergies_obj)
        if patient_allergies_add_form.is_valid():
          allergies_obj          = patient_allergies_add_form.save()
          success        = True
          error_message  = "Allergies Data Added Successfully"
          addData        = {
                            "id"                : allergies_obj.id,
                            "allergic_to"       : allergies_obj.allergic_to,
                            "reaction_observed" : allergies_obj.reaction_observed,
                            "edit"              : allergies_obj.get_edit_url(),
                            "del"               : allergies_obj.get_del_url()
          }
          data           = {'success'      : success, 
                            'error_message': error_message,
                            "form_errors"  : None,
                            "addData"      : addData
          }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Allergies data could not be added."
          form_errors   = ''
          for error in patient_allergies_add_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
  else:
    raise Http404("You need to Login")

@login_required
def patient_allergies_edit(request,id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                            = int(id)
        patient_allergies_obj         = PatientAllergies.objects.get(pk = id)
        patient_allergies_edit_form   = PatientAllergiesForm(instance = patient_allergies_obj)
        variable                      = RequestContext(request, 
        																					{"user" 									      :	user,
        																					 "patient_detail_obj"			      :	patient_allergies_obj.patient_detail ,
        																					 "patient_allergies_edit_form"  :	patient_allergies_edit_form, 
																									 "patient_allergies_obj" 		    :	patient_allergies_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientAllergies.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/allergies/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                            = int(id)
        patient_allergies_obj         = PatientAllergies.objects.get(pk = id)
        patient_allergies_edit_form   = PatientAllergiesForm(request.POST,instance = patient_allergies_obj)
        if patient_allergies_edit_form.is_valid():
          allergies_obj           = patient_allergies_edit_form.save()
          success                 = True
          error_message           = "Allergies Data Edited Successfully"
          addData                 = {
                                    "id"                : allergies_obj.id,
                                    "allergic_to"       : allergies_obj.allergic_to,
                                    "reaction_observed" : allergies_obj.reaction_observed,
                                    "edit"              : allergies_obj.get_edit_url(),
                                    "del"               : allergies_obj.get_del_url()
                                    }
          data                    = {
                                    'success'      : success, 
                                    'error_message': error_message,
                                    "form_errors"  : None,
                                    "addData"      : addData
                                    }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Allergies data could not be added."
          form_errors   = ''
          for error in patient_allergies_edit_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
  else:
    raise Http404("You need to Login")

@login_required
def patient_allergies_del(request,id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_allergies_obj   = PatientAllergies.objects.get(pk = id)
          patient_detail_obj      = patient_allergies_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientAllergies.DoesNotExist:
          raise Http404("BadRequest: Patient allergies Data Does Not Exist")
       patient_allergies_obj.delete()
       success        = True
       error_message  = "allergies Data Deleted Successfully"
       data           = {'success': success, 'error_message': error_message}
       json           = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")



@login_required
def patient_new_add(request):
  user = request.user
  print "Received a request to add a New Patient...."
  if request.method =="GET":
    patient_detail_obj      = PatientDetail()
    patient_detail_form     = PatientDetailForm(instance = patient_detail_obj)
    variable                = RequestContext(request, 
      																					{"user" :	user,
      																					"patient_detail_obj":	patient_detail_obj,
      																					"patient_detail_form": patient_detail_form
      																					}
      													)
    return render_to_response('patient/detail/add.html',variable)
  if request.method =="POST":
    patient_detail_form     = PatientDetailForm(request.POST)
    if patient_detail_form.is_valid():
      saved_patient = patient_detail_form.save()
      redirect_url  = saved_patient.get_patient_main_window_url()
      if request.is_ajax():
        print "REQUEST IS :: " , request.is_ajax()
        json = return_patient_json(saved_patient)
        return HttpResponse(json, content_type = 'application/json')
      else:
        print "REQUEST IS :: " , request.is_ajax()
        return HttpResponseRedirect(redirect_url)
    else:
      if request.is_ajax():
        json = return_patient_json(patient = None, success = False)
        return HttpResponse(json, content_type = 'application/json')
      else:
        variable                = RequestContext(request, { "user"  :	user, 
		    																					          "patient_detail_obj":	patient_detail_obj,
		    																					          "patient_detail_form": patient_detail_form  																								     }
		    													)
        return render_to_response('patient/detail/add.html', variable)
  else:
    raise Http404('Bad Request:: Unsupported Request Method.')


@login_required
def patient_detail_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      	= int(id)
        patient_detail_obj       	= PatientDetail.objects.get(pk = id)
        patient_detail_edit_form 	= PatientDetailForm(instance = patient_detail_obj)
        variable                	= RequestContext(request, 
 																				{"user"	:	user,
 																				"patient_detail_obj"	      :	patient_detail_obj ,
 																				 "patient_detail_edit_form"	: patient_detail_edit_form 
																				}
																	  )
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient detail Data Does Not Exist")
      return render_to_response('patient/detail/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                        = int(id)
        patient_detail_obj        = PatientDetail.objects.get(pk =id)
        patient_detail_edit_form  = PatientDetailForm(request.POST,instance = patient_detail_obj)
        if patient_detail_edit_form.is_valid():
          detail_object           = patient_detail_edit_form.save()
          json = return_patient_json(detail_object, success = True)
          print json
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error:: Patient Detail could not be edited."
          form_errors = ''
          for error in patient_detail_edit_form.errors:
            form_errors += '<p>' + error + '</p>'
          json = return_patient_json(detail_object = None, success = False)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient detail DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_detail_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                   = int(id)
          patient_detail_obj   = PatientDetail.objects.get(pk = id)
       except TypeError or ValueError or AttributeError:
         if request.is_ajax():
           success = False
           error_message = '''
                            ERROR!! Bad Request. Please refresh page and try again.
                           '''
           data = {"success": success, "error_message": error_message}
           json = simplejson.dumps(data)
           return HttpResponse(json, content_type = "application/json")
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
           return HttpResponse(json, content_type = "application/json")
         else:
           raise Http404("BadRequest: Patient detail Data Does Not Exist")
       if user.is_superuser:
         patient_detail_obj.delete()
         if request.is_ajax():
           success = True
           error_message = "Patient Deleted Successfully"
           data = {"success": success, "error_message": error_message}
           json = simplejson.dumps(data)
           return HttpResponse(json, content_type = "application/json")
         else:
           return HttpResponseRedirect('/')
       else:
         if request.is_ajax():
           success = False
           error_message = "ERROR ! No Priviliges to Delete..."
           data = {"success": success, "error_message": error_message}
           json = simplejson.dumps(data)
           return HttpResponse(json, content_type = "application/json")
         else:
           return HttpResponseRedirect('/')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")


################################################################################

################################################################################


@login_required
def patient_contact_add(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                        = int(id)
        patient_detail_obj        = PatientDetail.objects.get(pk =id)
        patient_contact_obj       = PatientContact(patient_detail = patient_detail_obj)
        patient_contact_add_form  = PatientContactForm(instance = patient_contact_obj)
        variable                  = RequestContext(request, {"user" 									:	user, 																														"patient_detail_obj"			:	patient_detail_obj , 																															"patient_contact_add_form" 	:	patient_contact_add_form, 
																														"patient_contact_obj" 			:	patient_contact_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/contact/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_contact_obj       = PatientContact(patient_detail = patient_detail_obj)
        patient_contact_add_form  = PatientContactForm(request.POST,instance = patient_contact_obj)
        if patient_contact_add_form.is_valid():
          contact_object                = patient_contact_add_form.save()
          success = True
          error_message = "Contact Saved Successfully"
          form_errors = None
          addData  = {
                   "id"           : contact_object.id,
                   'pat_id'       : contact_object.patient_detail.id,
                   "address_type" : contact_object.address_type,
                   "address"      : contact_object.address,
                   "city"         : contact_object.city,
                   "state"        : contact_object.state,
                   "country"      : contact_object.country,
                   "pincode"      : contact_object.pincode,
                   "edit"         : contact_object.get_patient_contact_edit_url(),
                   "del"          : contact_object.get_patient_contact_del_url(),
          }
          data = {"success"       : success, 
                  "error_message" : error_message, 
                  "form_errors"   : form_errors,
                   "addData"      : addData
                  }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error:: Contact could not be added."
          form_errors = ''
          for error in patient_contact_add_form.errors:
            form_errors += '<p>' + error + '</p>'
          data = {'success': success, 'error_message': error_message, 'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")

@login_required
def patient_contact_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                        = int(id)
        patient_contact_obj       = PatientContact.objects.get(pk = id)
        patient_contact_edit_form = PatientContactForm(instance = patient_contact_obj)
        patient_detail_obj        = patient_contact_obj.patient_detail
        variable                  = RequestContext(request, 
        																						{"user" :	user,
        																						 "patient_detail_obj"			  :	patient_detail_obj , 																											 "patient_contact_edit_form":	patient_contact_edit_form, 
																										 "patient_contact_obj" 			:	patient_contact_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientContact.DoesNotExist:
        raise Http404("BadRequest: Patient contact Data Does Not Exist")
      return render_to_response('patient/contact/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                         = int(id)
        patient_contact_obj        = PatientContact.objects.get(pk =id)
        patient_detail_obj       	 = patient_contact_obj.patient_detail
        patient_contact_edit_form  = PatientContactForm(request.POST,instance = patient_contact_obj)
        if patient_contact_edit_form.is_valid():
          contact_object           = patient_contact_edit_form.save()
          success 			= True
          error_message = "Contact Saved Successfully"
          form_errors 	= None
          success = True
          error_message = "Contact Saved Successfully"
          form_errors = None
          data = {"success"       : success, 
                  "error_message" : error_message, 
                  "form_errors"   : form_errors,
                   "id"           : contact_object.id,
                   'pat_id'       : contact_object.patient_detail.id,
                   "address_type" : contact_object.address_type,
                   "address"      : contact_object.address,
                   "city"         : contact_object.city,
                   "state"        : contact_object.state,
                   "country"      : contact_object.country,
                   "pincode"      : contact_object.pincode,
                   "edit"         : contact_object.get_edit_url(),
                   "del"          : contact_object.get_del_url()
                  }
          json 					= simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error:: Contact could not be added."
          form_errors = ''
          for error in patient_contact_edit_form.errors:
            form_errors += '<p>' + error + '</p>'
          data = {'success'				: success, 
          				'error_message'	: error_message, 
          				'form_errors': form_errors
          			}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientContact.DoesNotExist:
        raise Http404("BadRequest: Requested Patient contact DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_contact_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_contact_obj     = PatientContact.objects.get(pk = id)
          patient_detail_obj      = patient_contact_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientContact.DoesNotExist:
          raise Http404("BadRequest: Patient contact Data Does Not Exist")
       patient_contact_obj.delete()
       success        = True
       error_message  = "contact Data Deleted Successfully"
       data           = {'success': success, 'error_message': error_message}
       json           = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")


################################################################################

################################################################################


@login_required
def patient_email_and_fax_add(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_email_and_fax_obj       = PatientEmailAndFax(patient_detail = patient_detail_obj)
        patient_email_and_fax_add_form  = PatientEmailAndFaxForm(instance = patient_email_and_fax_obj)
        variable                = RequestContext(request, {"user" 									:	user, 																													"patient_detail_obj"			:	patient_detail_obj , 																														"patient_email_and_fax_add_form" 	:	patient_email_and_fax_add_form, 
																													"patient_email_and_fax_obj" 			:	patient_email_and_fax_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/email_and_fax/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_email_and_fax_obj       = PatientEmailAndFax(patient_detail = patient_detail_obj)
        patient_email_and_fax_add_form  = PatientEmailAndFaxForm(request.POST,instance = patient_email_and_fax_obj)
        if patient_email_and_fax_add_form.is_valid():
          email_and_fax_object                = patient_email_and_fax_add_form.save()
          success = True
          error_message = "Email And Fax Saved Successfully"
          form_errors = None
          data = {'success': success, 'error_message': error_message, 'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error:: Email and Fax detail could not be added."
          form_errors = ''
          for error in patient_email_and_fax_add_form.errors:
            form_errors += '<p>' + error + '</p>'
          data = {'success': success, 'error_message': error_message, 'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")

@login_required
def patient_email_and_fax_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_email_and_fax_obj       = PatientEmailAndFax(pk = id)
        patient_email_and_fax_edit_form = PatientEmailAndFaxForm(instance = patient_email_and_fax_obj)
        patient_detail_obj      = patient_email_and_fax_obj.patient_detail
        variable                = RequestContext(request, {"user" :	user,
        																										"patient_detail_obj"			:	patient_detail_obj , 																															"patient_email_and_fax_edit_form"	:	patient_email_and_fax_edit_form, 
																														"patient_email_and_fax_obj" 			:	patient_email_and_fax_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientEmailAndFax.DoesNotExist:
        raise Http404("BadRequest: Patient email_and_fax Data Does Not Exist")
      return render_to_response('patient/email_and_fax/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                        = int(id)
        patient_email_and_fax_obj        = PatientEmailAndFax.objects.get(pk =id)
        patient_detail_obj       = patient_email_and_fax_obj.patient_detail
        patient_email_and_fax_edit_form  = PatientEmailAndFaxForm(request.POST,instance = patient_email_and_fax_obj)
        if patient_email_and_fax_edit_form.is_valid():
          email_and_fax_object                = patient_email_and_fax_edit_form.save()
          return HttpResponseRedirect(request.get_full_path())
        else:
          variable        = RequestContext(request, {"patient_email_and_fax_edit_form"	:	patient_email_and_fax_edit_form,
																										 "user"											:	user,
																										 'patient_detail_obj'				: patient_detail_obj
																										})
          return render_to_response("patient/email_and_fax/edit.html", variable)
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientEmailAndFax.DoesNotExist:
        raise Http404("BadRequest: Requested Patient email_and_fax DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_email_and_fax_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_email_and_fax_obj       = PatientEmailAndFax(pk = id)
          patient_detail_obj      = patient_email_and_fax_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientEmailAndFax.DoesNotExist:
          raise Http404("BadRequest: Patient email_and_fax Data Does Not Exist")
       patient_email_and_fax_obj.delete()
       success = True
       error_message = "email_and_fax Data Deleted Successfully"
       data = {'success': success, 'error_message': error_message}
       json = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")


################################################################################

################################################################################


@login_required
def patient_guardian_add(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_guardian_obj       = PatientGuardian(patient_detail = patient_detail_obj)
        patient_guardian_add_form  = PatientGuardianForm(instance = patient_guardian_obj)
        variable                = RequestContext(request, 
        																						{ "user" 									  : user,
        																						 "patient_detail_obj"		    : patient_detail_obj ,
        																						 "patient_guardian_add_form": patient_guardian_add_form, 
																									  "patient_guardian_obj" 		  : patient_guardian_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/guardian/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_guardian_obj       = PatientGuardian(patient_detail = patient_detail_obj)
        patient_guardian_add_form  = PatientGuardianForm(request.POST,instance = patient_guardian_obj)
        if patient_guardian_add_form.is_valid():
          guardian_object                = patient_guardian_add_form.save()
          success = True
          error_message = "Guardian data Saved Successfully"
          form_errors = None
          addData     = {
                         "id"                   : guardian_object.id,
                          "edit"                : guardian_object.get_edit_url(),
                          "del"                 : guardian_object.get_del_url(),
                          "guardian_name"       : guardian_object.guardian_name,
                          "relation_to_guardian": guardian_object.relation_to_guardian,
                          "guardian_phone"      : guardian_object.guardian_phone
          }
          data = {'success'             : success, 
                  'error_message'       : error_message, 
                  'form_errors'         : form_errors,
                  "addData"             : addData
          }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error:: Guardian could not be added."
          form_errors = ''
          for error in patient_guardian_add_form.errors:
            form_errors += '<p>' + error + '</p>'
          data = {'success': success, 'error_message': error_message, 'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")

@login_required
def patient_guardian_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_guardian_obj       = PatientGuardian.objects.get(pk = id)
        patient_guardian_edit_form = PatientGuardianForm(instance = patient_guardian_obj)
        patient_detail_obj      	 = patient_guardian_obj.patient_detail
        variable                   = RequestContext(request, {"user" 										 :	user,
        																										"patient_detail_obj"			   :	patient_detail_obj , 																															"patient_guardian_edit_form" :	patient_guardian_edit_form, 
																														"patient_guardian_obj" 			 :	patient_guardian_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientContact.DoesNotExist:
        raise Http404("BadRequest: Patient guardian Data Does Not Exist")
      return render_to_response('patient/guardian/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                          = int(id)
        patient_guardian_obj        = PatientGuardian.objects.get(pk =id)
        patient_detail_obj       		= patient_guardian_obj.patient_detail
        patient_guardian_edit_form  = PatientGuardianForm(request.POST,instance = patient_guardian_obj)
        if patient_guardian_edit_form.is_valid():
          guardian_object                = patient_guardian_edit_form.save()
          success = True
          error_message = "Guardian data Saved Successfully"
          form_errors = None
          addData     = {
                         "id"                   : guardian_object.id,
                          "edit"                : guardian_object.get_edit_url(),
                          "del"                 : guardian_object.get_del_url(),
                          "guardian_name"       : guardian_object.guardian_name,
                          "relation_to_guardian": guardian_object.relation_to_guardian,
                          "guardian_phone"      : guardian_object.guardian_phone
          }
          data = {'success'             : success, 
                  'error_message'       : error_message, 
                  'form_errors'         : form_errors,
                  "addData"             : addData
          }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error:: Guardian could not be added."
          form_errors = ''
          for error in patient_guardian_edit_form.errors:
            form_errors += '<p>' + error + '</p>'
          data = {'success': success, 'error_message': error_message, 'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientContact.DoesNotExist:
        raise Http404("BadRequest: Requested Patient guardian DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_guardian_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_guardian_obj    = PatientGuardian(pk = id)
          patient_detail_obj      = patient_guardian_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientContact.DoesNotExist:
          raise Http404("BadRequest: Patient guardian Data Does Not Exist")
       patient_guardian_obj.delete()
       success = True
       error_message = "guardian Data Deleted Successfully"
       data = {'success': success, 'error_message': error_message}
       json = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")


################################################################################
################################################################################


@login_required
def patient_phone_add(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_phone_obj       = PatientPhone(patient_detail = patient_detail_obj)
        patient_phone_add_form  = PatientPhoneForm(instance = patient_phone_obj)
        variable                = RequestContext(request, 
        																					{"user" 									:	user,
        																					 "patient_detail_obj"			:	patient_detail_obj ,
        																					 "patient_phone_add_form" :	patient_phone_add_form, 
																									 "patient_phone_obj" 		  :	patient_phone_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/phone/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_phone_obj       = PatientPhone(patient_detail = patient_detail_obj)
        patient_phone_add_form  = PatientPhoneForm(request.POST,instance = patient_phone_obj)
        if patient_phone_add_form.is_valid():
          phone_obj          = patient_phone_add_form.save()
          success        = True
          error_message  = "Phone Data Added Successfully"
          addData        = {
                            "id"           : phone_obj.id,
                            "phone_type"   : phone_obj.phone_type,
                            "ISD_Code"     : phone_obj.ISD_Code,
                            "STD_Code"     : phone_obj.STD_Code,
                            "phone"        : phone_obj.phone,
                            "edit"         : phone_obj.get_edit_url(),
                            "del"          : phone_obj.get_del_url()
          }
          data           = {'success'      : success, 
                            'error_message': error_message,
                            "form_errors"  : None,
                            "addData"      : addData
          }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Phone data could not be added."
          form_errors   = ''
          for error in patient_phone_add_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))

@login_required
def patient_phone_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_phone_obj       = PatientPhone.objects.get(pk = id)
        patient_phone_edit_form = PatientPhoneForm(instance = patient_phone_obj)
        patient_detail_obj      = patient_phone_obj.patient_detail
        variable                = RequestContext(request, {"user" 					          :	user, 
                                                            "patient_detail_obj"			:	patient_detail_obj , 																															"patient_phone_edit_form"	:	patient_phone_edit_form, 
																														"patient_phone_obj" 			:	patient_phone_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientPhone.DoesNotExist:
        raise Http404("BadRequest: Patient Phone Data Does Not Exist")
      return render_to_response('patient/phone/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                        = int(id)
        patient_phone_obj        = PatientPhone.objects.get(pk =id)
        patient_phone_edit_form  = PatientPhoneForm(request.POST,instance = patient_phone_obj)
        patient_detail_obj       = patient_phone_obj.patient_detail
        if patient_phone_edit_form.is_valid():
          phone_obj          = patient_phone_edit_form.save()
          success = True
          error_message = "Phone Data Edited Successfully"
          data           = {'success'      : success, 
                            'error_message': error_message,
                            "form_errors"  : None,
                            "id"           : phone_obj.id,
                            "phone_type"   : phone_obj.phone_type,
                            "ISD_Code"     : phone_obj.ISD_Code,
                            "STD_Code"     : phone_obj.STD_Code,
                            "phone"        : phone_obj.phone,
                            "edit"         : phone_obj.get_patient_phone_edit_url(),
                            "del"          : phone_obj.get_patient_phone_del_url()
                           }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success = False
          error_message = "Error Occured. Phone data could not be added."
          form_errors   = ''
          for error in patient_phone_edit_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = {'success': success, 'error_message': error_message,'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')          
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientPhone.DoesNotExist:
        raise Http404("BadRequest: Requested Patient Phone DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. request's AJAX status was:: ", request.is_ajax())


@login_required
def patient_phone_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_phone_obj       = PatientPhone(pk = id)
          patient_detail_obj      = patient_phone_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientPhone.DoesNotExist:
          raise Http404("BadRequest: Patient Phone Data Does Not Exist")
       patient_phone_obj.delete()
       success = True
       error_message = "Phone Data Deleted Successfully"
       data = {'success': success, 'error_message': error_message}
       json = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")



################################################################################

@login_required
def patient_demographics_add(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                   = int(id)
        patient_detail_obj   = PatientDetail.objects.get(pk =id)
        demographics_obj     = PatientDemographicsData.objects.filter(patient_detail = patient_detail_obj)
        if demographics_obj:
          patient_demographics_data_obj    = demographics_obj[0]
          patient_demographics_data_form   = PatientDemographicsDataForm(instance = patient_demographics_data_obj)
          variable = {'user'                      : user, 
                      'patient_detail_obj'        : patient_detail_obj,
                      'patient_demographics_data_obj'  : patient_demographics_data_obj,
                      'patient_demographics_data_form' : patient_demographics_data_form,
                      'button_label'              : 'Edit',
                      'action'                    : patient_demographics_data_obj.get_edit_url(),
                      'canDel'                    : True,
                      "addUrl"                    : None,
                      'editUrl'                   : patient_demographics_data_obj.get_edit_url(),
                      'delUrl'                    : patient_demographics_data_obj.get_del_url()
                      }
        else:
          patient_demographics_data_obj   = PatientDemographicsData(patient_detail = patient_detail_obj)
          patient_demographics_data_form  = PatientDemographicsDataForm(instance = patient_demographics_data_obj)
          variable                        = RequestContext(request, 
                                          {"user" 									       :	user,
                                          "patient_detail_obj"			       :	patient_detail_obj ,
                                          "patient_demographics_data_form"  :	patient_demographics_data_form, 
                                          "patient_demographics_data_obj"  :	patient_demographics_data_obj ,
                                          'button_label'                  :  "Add",
                                          "action"                        : patient_detail_obj.get_patient_demographics_data_add_url(),
                                          "addUrl"                        : patient_detail_obj.get_patient_demographics_data_add_url(),
                                          'canDel'                        : False,
                                          'editUrl'                       : None,
                                          'delUrl'                        : None
                                           })
        return render_to_response('patient/demographics_data/add_or_edit_form.html', variable)
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                              = int(id)
        patient_detail_obj              = PatientDetail.objects.get(pk =id)
        patient_demographics_data_obj   = PatientDemographicsData(patient_detail = patient_detail_obj)
        patient_demographics_data_form  = PatientDemographicsDataForm(request.POST,instance = patient_demographics_data_obj)
        if patient_demographics_data_form.is_valid():
          try:
            demographics_obj  = patient_demographics_data_form.save()
#            json              = generate_json_for_datagrid(demographics_obj)
            success       = True
            error_message = "Demographics Data Added Successfully"
            form_errors   = ''
            data = { 'success'      : success, 
                     'error_message': error_message,
                     'form_errors'  : form_errors,
                     'canDel'       : True,
                     'addUrl'       : None,
                     'editUrl'      : demographics_obj.get_edit_url(),
                     'delUrl'       : demographics_obj.get_del_url(),
                   }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type = 'application/json')
          except (DemographicsDataExistsError):
            success       = False
            error_message = "Demographics Data Already Exists ! Cannot add more.."
            form_errors   = ''
            data = { 'success'      : success, 
                     'error_message': error_message,
                     'form_errors'  : form_errors
                   }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. DemographicsData data could not be added."
          form_errors   = ''
          for error in patient_demographics_data_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))



@login_required
def patient_demographics_edit(request, id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                             = int(id)
        patient_demographics_data_obj       = PatientDemographicsData.objects.get(pk = id)
        patient_demographics_data_form = PatientDemographicsDataForm(instance = patient_demographics_data_obj)
        patient_detail_obj                  = patient_demographics_data_obj.patient_detail
        variable                            = RequestContext(request, 
                                                {"user":user,
                                                "patient_detail_obj"             : patient_detail_obj ,
                                                "patient_demographics_data_form" : patient_demographics_data_form, 
                                                "patient_demographics_data_obj"  :patient_demographics_data_obj ,
                                                'action'                          : patient_demographics_data_obj.get_edit_url(),
                                                'button_label'                    : "Edit",
                                                'canDel'                          : True,
                                                'addUrl'                          : None,
                                                'editUrl'                         : patient_demographics_data_obj.get_edit_url(),
                                                'delUrl'                          : patient_demographics_data_obj.get_del_url(),
                                               })
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientDemographicsData.DoesNotExist:
        raise Http404("BadRequest: Patient DemographicsData Data Does Not Exist")
      return render_to_response('patient/demographics_data/add_or_edit_form.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                              = int(id)
        patient_demographics_data_obj        = PatientDemographicsData.objects.get(pk =id)
        patient_demographics_data_form  = PatientDemographicsDataForm(request.POST,instance = patient_demographics_data_obj)
        patient_detail_obj              = patient_demographics_data_obj.patient_detail
        if patient_demographics_data_form.is_valid():
          demographics_obj  = patient_demographics_data_form.save()
          success       = True
          error_message = "Demographics Data Edited Successfully"
          form_errors   = ''
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
#          data             = generate_json_for_datagrid(demographics_obj)
          json              = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. Demographics Data data could not be added."
          form_errors   = ''
          for error in patient_demographics_data_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = {'success': success, 'error_message': error_message,'form_errors': form_errors}
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')          
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDemographicsData.DoesNotExist:
        raise Http404("BadRequest: Requested Patient Demographics Data DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. request's AJAX status was:: ", request.is_ajax())


@login_required
def patient_demographics_del(request, id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_demographics_obj = PatientDemographicsData.objects.get(pk = id)
          patient_detail_obj       = patient_demographics_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientDemographicsData.DoesNotExist:
          raise Http404("BadRequest: Patient Demographics Data Does Not Exist")
       patient_demographics_obj.delete()
       success = True
       error_message = "Demographics Data Deleted Successfully"
       data = {'success'        : success, 
                'error_message' : error_message, 
                'addUrl'        : patient_detail_obj.get_patient_demographics_data_add_url(),
                'canDel'        : False, 
                'editUrl'       : None, 
                'delUrl'        : None
               }
       json = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")


################################################################################


@login_required
def patient_search(request, search_by, search_for):
    if request.user:
        user                            = request.user
        search_by       = request.GET['search_by']
        search_for      = request.GET['search_for']

        if search_by =="first_name":
            try:
                patient_obj     = PatientDetail.objects.filter(first_name__icontains = search_for)
                variable                        = RequestContext(request, {'patient_obj':patient_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

        elif search_by =="middle_name":
            try:
                patient_obj     = PatientDetail.objects.filter(middle_name__icontains = search_for)
                variable                        = RequestContext(request, {'patient_obj':patient_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

        elif search_by =="last_name":
            try:
                patient_obj     = PatientDetail.objects.filter(last_name__icontains = search_for)
                variable                        = RequestContext(request, {'patient_obj':patient_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

        elif search_by =="hospital_id":
            try:
                patient_obj     = PatientDetail.objects.filter(patient_hospital_id__icontains = search_for)
                variable                        = RequestContext(request, {'patient_obj':patient_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

        elif search_by =="phone":
            try:
                phone_obj               =       PatientPhone.objects.filter(phone__icontains = search_for)
                variable                        = RequestContext(request, {'phone_obj':phone_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

        elif search_by =="guardian_name":
            try:
                guardian_obj    = PatientGuardian.objects.filter(guardian_name__icontains = search_for)
                variable                        = RequestContext(request, {'guardian_obj':guardian_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

        elif search_by =="city":
            try:
                contact_obj     = PatientContact.objects.filter(city__icontains = search_for)
                variable                        = RequestContext(request, {'contact_obj':contact_obj, 'user':user})
                return render_to_response('patient/patient_search_result.html',variable)
            except ValueError or TypeError or AttributeError:
                raise Http404("Please enter a correct search term")

    else:
        raise Http404("Please Log in")


################################################################################


@login_required
def patient_admission_add(request, id=None):
    if request.is_ajax():
        if request.user:
            user = request.user
            if request.method =='GET':
                get_data   = request.GET.copy()
                try:
                  if not id:
                    patient_id  = int(request.GET.get('patient_id'))
                  else:
                    patient_id = int(id)
                  patient_obj = PatientDetail.objects.get(pk = patient_id)
                except(ValueError, TypeError, KeyError, AttributeError): 
                  message = '''
                             Server Error !!. Invalid Request parameters.
                             Please check your request and try again..
                           '''
                  return HttpResponse(message)
                except(PatientDetail.DoesNotExist):
                  return HttpResponse("Bad Request. The requested patient data does not exist.")
                all_admissions = Admission.objects.filter(patient_detail = patient_obj).filter(admission_closed = False)
                if len(all_admissions) >0:
                  error_message              = "Admission is still active. Cannot add more"
                  patient_admission_add_form = None
                  adm_obj                    = None
                else:
                  error_message               = None
                  adm_obj                     = Admission(patient_detail = patient_obj)
                  patient_admission_add_form  = AdmissionForm(instance = adm_obj)
                  print 'received GET for patient with id ' + str(patient_id)
                variable   = RequestContext(request, 
                                            {'user'                      : user,
                                             'patient_admission_add_form': patient_admission_add_form,
                                             'patient_detail_obj'        : patient_obj,
                                             'adm_obj'                   : adm_obj,
                                             'error_message'             : error_message
                                             })
                return render_to_response('admission/detail/add.html', variable)
            elif request.method == "POST":
                try:
                  if not id:
                    patient_id    = int(request.POST['patient_id'])
                  else:
                    patient_id = int(id)
                  patient_obj                  = PatientDetail.objects.get(pk = patient_id)
                except(ValueError, TypeError, KeyError, AttributeError): 
                   raise Http404("Bad Request. Invalid Request Parameters.")
                except(PatientDetail.DoesNotExist):
                   raise Http404("Bad Request. The requested patient data does not exist.")
                adm_obj                      = Admission(patient_detail = patient_obj)
                request_post_copy            = request.POST.copy()
                time                         = request.POST.get('time_of_admission')[1:]
                request_post_copy['time_of_admission']  = time
                patient_admission_add_form   = AdmissionForm(request_post_copy, instance = adm_obj)
                print request.POST
                if patient_obj.has_active_admission()!='0':
                  error_message   =  '''
                                        This patient has an active Admission. 
                                        You cannot add admission now.
                                     '''
                  success         = False
                  form_errors     = patient_admission_add_form.errors
                else:
                  if patient_admission_add_form.is_valid():
                      saved_adm_obj   = patient_admission_add_form.save()
                      print "DATE OF ADMISSION IS:: " + saved_adm_obj.date_of_admission.isoformat()
                      print "TIME OF ADMISSION IS:: " + saved_adm_obj.time_of_admission.isoformat()
                      error_message   = 'Admission added successfully'
                      success         = True
                      form_errors     = patient_admission_add_form.errors
                      data = {
                         'error_message'     : error_message,
                         'success'           : success,
                         'form_errors'       : form_errors,
                         'id'                : saved_adm_obj.id,
                         'date_of_admission' : saved_adm_obj.date_of_admission.isoformat(),
                         'time_of_admission' : saved_adm_obj.time_of_admission.isoformat(),
                         'admission_closed'  : saved_adm_obj.admission_closed,
                         'admitting_surgeon' : saved_adm_obj.admitting_surgeon.surgeon_name,
                         'hospital'          : saved_adm_obj.hospital,
                         'room_or_ward'      : saved_adm_obj.room_or_ward,
                         'home'              : saved_adm_obj.get_admission_main_window_url(),
                         'edit'              : saved_adm_obj.get_admission_edit_url(),
                         'del'               : saved_adm_obj.get_admission_del_url()
                        }
                      json = simplejson.dumps(data)
                      return HttpResponse(json, content_type = 'application/json')
                  else:
                      error_message   = '''
                                           Error ! Admission could not be added:
                                           Submitted Data Did not validate.
                                        '''
                      success         = False
                      form_errors     = patient_admission_add_form.errors
                      print form_errors
                data = {
                         'error_message': error_message,
                         'success'      : success,
                         'form_errors'  : form_errors
                        }
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type = 'application/json')
            else:
                return HttpResponse('Invalid Request')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render_to_response('admission/detail/add.html', variable)
