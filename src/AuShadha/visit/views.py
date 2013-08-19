##--------------------------------------------------------------
# AuShadha Views for Visit Details and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# License : GNU - GPL Version 3
# Date: 27-12-2012
##---------------------------------------------------------------


# General Django Imports----------------------------------

from django.shortcuts                import render_to_response
from django.http                     import Http404, HttpResponse, HttpResponseRedirect
from django.template                 import RequestContext
from django.template.loader          import get_template
from django.template                 import Context
#from django.core.context_processors import csrf
from django.contrib.auth.models      import User
#from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.views       import logout
from django.contrib.auth.decorators  import login_required
from django.forms.models             import modelformset_factory
from django.forms.formsets           import formset_factory
from django.core.paginator           import Paginator
from django.utils                    import simplejson

# General Module imports-----------------------------------
from datetime                        import datetime, date, time
#import ho.pisa                      as pisa
import xhtml2pdf.pisa                as pisa 
import cStringIO                     as StringIO



# Application Specific Model Imports-----------------------

from aushadha_users.models            import AuShadhaUser
from clinic.models                   import Clinic, Staff
from visit.models                    import *
from patient.models                  import *
from admission.models                import Admission
from physician.models                import PhysicianDetail
from inv_and_imaging.models          import LabInvestigationRegistry, ImagingInvestigationRegistry

#from complaints_and_history.models                  import *
#from phyexam.models                  import PhyExam, RegExam
#from detail_exam.models              import *

#TOTAL_COMPLAINTS_FORM = 1
#VisitComplaintsFormset = modelformset_factory(VisitComplaints, VisitComplaintsForm, extra  = TOTAL_COMPLAINTS_FORM +2, max_num = 10)

# Module Vars:
complaint_add_icon_template     = get_template('visit/snippets/icons/complaints_add.html')
complaint_remove_icon_template = get_template('visit/snippets/icons/complaints_remove.html')


# views start here;;

@login_required
def visit_list(request):
  if request.user:
    user = request.user
    if request.method == "GET":
      visit_obj = VisitDetail.objects.all().order_by('visit_date')
      variable = RequestContext(request, {'user':user,
                  'visit_obj':visit_obj,
                  })
      return render_to_response('visit/visit_list.html',variable)
    else:
      raise Http404("Bad Request:: " + str(request.method) + " ")
  else:
    return HttpResponseRedirect('/AuShadha/login/')

@login_required
def visit_home(request,id = 'id'):
  pass

################################################################################
@login_required
def render_visit_tree(request,id = None):
  if request.method=="GET" and request.is_ajax():
    if id:
      patient_id = int(id)
    else:
      try:
        patient_id = int(request.GET.get('patient_id'))
        pat_obj = PatientDetail.objects.get(pk = patient_id)
      except(AttributeError, NameError, KeyError, TypeError,ValueError):
        raise Http404("ERROR! Bad Request Parameters")
      except(AttributeError, NameError, KeyError, TypeError,ValueError):
        raise Http404("ERROR! Requested Patient Data Does not exist")

      adm_obj               = Admission.objects.filter(patient_detail = pat_obj)
      visit_obj             = VisitDetail.objects.filter(patient_detail = pat_obj)

      prev_visit_obj             = VisitDetail.objects.filter(patient_detail = pat_obj).filter(is_active = False)
      active_visit_obj           = VisitDetail.objects.filter(patient_detail = pat_obj).filter(is_active = True)


      demographics_obj      = PatientDemographicsData.objects.filter(patient_detail = pat_obj)
      social_history_obj    = PatientSocialHistory.objects.filter(patient_detail = pat_obj)
      family_history_obj    = PatientFamilyHistory.objects.filter(patient_detail = pat_obj)
      medical_history_obj   = PatientMedicalHistory.objects.filter(patient_detail = pat_obj)
      surgical_history_obj  = PatientSurgicalHistory.objects.filter(patient_detail = pat_obj)

      medication_list_obj   = PatientMedicationList.objects.filter(patient_detail = pat_obj)
      allergy_obj           = PatientAllergies.objects.filter(patient_detail = pat_obj)

      pat_inv_obj        = VisitInv.objects.filter(visit_detail__patient_detail = pat_obj)
      pat_imaging_obj    = VisitImaging.objects.filter(visit_detail__patient_detail = pat_obj)

      data = {
         "identifier": "id"   ,
         "label"     : "name" ,
         "items"     : [
                        {"name"  : "Procedures"      , "type":"application", "id":"PROC" ,
                        "len"   : 1,
                        "addUrl": None,
                        },

                        {"name"  : "History"      , "type":"application", "id":"HISTORY" ,
                        "len"   : 1,
                        "addUrl": None,
                        },

                        {"name"  : "Medication" , "type":"application", "id":"MEDICATION_LIST" ,
                        "len"   : 1,
                        "addUrl": None,
                        },

                        {"name"  : "Investigation" , "type":"application", "id":"INV" ,
                        "len"   : 1,
                        "addUrl": None,
                        },

                        {"name"  : "Imaging"      , "type":"application", "id":"IMAG" ,
                        "len"   : 1,
                        "addUrl": None,
                        },

                        #{"name"  : "Media" , "type":"application", "id":"MEDIA" ,
                        #"len"   : 1,
                        #"addUrl": None,
                        #'children':[
                            #{"name"  : "Documents" , "type":"patient_documents_module", "id":"DOCS" ,
                            #"len"   : 1,
                            #"addUrl": None,
                            #},
                            #{"name"  : "Images" , "type":"patient_images_module", "id":"IMAGES" ,
                            #"len"   : 1,
                            #"addUrl": None,
                            #}
                         #]
                        #}
                    ]
      }

      tree_item_list = data['items']

      if pat_obj.can_add_new_visit():
        dict_to_append = {"name"    : "New OPD Visit" ,
                            "type"  : "application"   ,
                            "id"    : "NEW_OPD_VISIT" ,
                            "len"   : len(visit_obj)  ,
                            "addUrl": pat_obj.get_patient_visit_add_url()
                    }
        tree_item_list.insert(0, dict_to_append)

      if active_visit_obj:
        active_visits = VisitDetail.objects.filter(patient_detail=pat_obj).filter(is_active = True)
        active_visits_base_dict = {"name"   : "Active Visits",
                                  "type"    : "application", 
                                  "id"      : "ACTIVE_VISITS",
                                  "len"     : True,
                                  "addUrl"  : None,
                                  'editUrl' : None,
                                  'delUrl'  : None,
                                  'children':[]
                                  }
        for active_visit in active_visits:
          base_dict = {"name"     : active_visit.visit_date.date().isoformat()    , 
                        "type"    : "active_visit", 
                        "id"      : "ACTIVE_VISITS_"+ str(active_visit.id),
                        "len"     : True,
                        "addUrl"  : None,
                        'editUrl' : active_visit.get_edit_url(),
                        'delUrl'  : active_visit.get_del_url(),
                        'children':[
                          {"name" : "Add Follow-Up" , 
                          "type"  : "visit_follow_up_add", 
                          "id"    : "VISIT_FOLLOW_UP_ADD_"+ str(active_visit.id),
                          "len"   : 1,
                          "addUrl": active_visit.get_visit_detail_visit_follow_up_add_url(),
                          },

                          {"name"  : "Orders" , 
                           "type"  : "application", 
                           "id"    : "ACTIVE_VISIT_" + str(active_visit.id) +"_ORDERS_AND_PRESCRIPTION" ,
                           "len"   : 1,
                           "addUrl": None,
                          },

                          {"name" : "Close" , 
                          "type"  : "close_visit", 
                          "id"    : "VISIT_CLOSE_"+ str(active_visit.id) ,
                          "len"   : 1,
                          "addUrl": active_visit.get_visit_detail_close_url(),
                          },

                          #{"name"      : "Edit" , 
                          #"type"       : "visit", 
                          #"id"         : "ACTIVE_VISIT_" + str(active_visit.id) ,
                          #"len"        : 1,
                          #"addUrl"     : None,
                          #"absoluteUrl": active_visit.get_absolute_url(),
                          #"editUrl"    : active_visit.get_edit_url(),
                          #"deUrl"      : active_visit.get_del_url()
                          #},

                          #{"name"  : "Diagnosis" , "type":"application", "id":"DIAG" ,
                          #"len"   : 1,
                          #"addUrl": None,
                          #},

                          #{"name"  : "Advice" , "type":"advice","id":"ADVICE" ,
                          #"len"   : 1,
                          #"addUrl": None,
                          #},

                          #{"name"  : "Procedure" , "type":"procedure", "id":"PROC" ,
                          #"len"   : 1,
                          #"addUrl": None,
                          #},

                          #{"name"  : "Calendar" , "type":"application", "id":"CAL" ,
                          #"len"   : 1,
                          #"addUrl": None,
                          #},
                      ]
                    }
          active_visits_base_dict['children'].append(base_dict)

          if active_visit.has_fu_visits():
            fu_visit = active_visit.has_fu_visits()
            fu_base_dict = {"name"        : "Follow-ups" , 
                            "type"        : "fu_visits", 
                            "id"          : "",
                            "len"         : 1,
                            "addUrl"      : None,
                            "absoluteUrl" : None,
                            "children"    : []
                          }
            fu_sub_dict = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
            base_dict['children'].append(fu_base_dict)
            
            for fu in fu_visit:
              fu_dict_to_append = fu_sub_dict.copy()
              print fu.__class__
              print "Edit URL for FU is: ", fu.get_edit_url()
              print "Del URL for FU is: ", fu.get_del_url()

              fu_dict_to_append = {"name"   : fu.visit_date.date().isoformat(), 
                                  "type"    : "fu_visit", 
                                  "id"      : "FU_VISIT_"+ str(fu.id),
                                  "editUrl" : fu.get_edit_url(),
                                  "delUrl"  : fu.get_del_url(),
                                  "children": [{"name"  : "Orders"   , 
                                                "type"  : "application"             , 
                                                "id"    : "FU_VISIT_" + str(fu.id) +"_ORDERS_AND_PRESCRIPTION" ,
                                                "len"   : 1                         ,
                                                "addUrl": None,
                                               }]
                                  }
              fu_base_dict['children'].append(fu_dict_to_append)

        tree_item_list.insert(1, active_visits_base_dict)
        #tree_item_list.insert(1, base_dict)

      if prev_visit_obj:
        base_dict     = {"name"  : "Closed Visits"  , "type":"application", "id":"CLOSED_VISITS", 'children':[]}
        sub_dict = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
        for visit in prev_visit_obj:
          dict_to_append = sub_dict.copy()
          dict_to_append['name']        = visit.visit_date.date().isoformat() + "("+ visit.op_surgeon.__unicode__() +")"
          dict_to_append['id']          = "CLOSED_VISIT_"+ unicode(visit.id)
          dict_to_append['absoluteUrl'] = visit.get_absolute_url()
          dict_to_append['editUrl']     = visit.get_edit_url()
          dict_to_append['editUrl']     = visit.get_edit_url()
          dict_to_append['delUrl']      = visit.get_del_url()
          dict_to_append['children']    = [{"name"  : "Orders"  , 
                                            "type"  : "application"            , 
                                            "id"    : "CLOSED_VISIT_" + str(visit.id) +"_ORDERS_AND_PRESCRIPTION" ,
                                            "len"   : 1,
                                            "addUrl": None,
                                           }]
          base_dict['children'].append(dict_to_append)
          if visit.has_fu_visits():
            fu_visit = visit.has_fu_visits()
            fu_base_dict = {"name"        : "Follow-ups" , 
                            "type"        : "fu_visits", 
                            "id"          : "CLOSED_FOLLOW_UP_VISITS_"+str(visit.id),
                            "len"         : 1,
                            "addUrl"      : None,
                            "absoluteUrl" : None,
                            "children"    : []
                          }
            fu_sub_dict = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
            dict_to_append['children'].append(fu_base_dict)
            
            for fu in fu_visit:
              fu_dict_to_append = fu_sub_dict.copy()
              fu_dict_to_append = {"name"   : fu.visit_date.date().isoformat(), 
                                  "type"    : "fu_visit", 
                                  "id"      : "CLOSED_FU_VISIT_"+ str(fu.id),
                                  "editUrl" : fu.get_edit_url(),
                                  "delUrl"  : fu.get_del_url(),
                                  "children": [{"name"  : "Orders"  , 
                                              "type"  : "application"            , 
                                              "id"    : "CLOSED_FU_VISIT_" + str(fu.id) +"_ORDERS_AND_PRESCRIPTION" ,
                                              "len"   : 1,
                                              "addUrl": None,
                                             }]
                                  }
              fu_base_dict['children'].append(fu_dict_to_append)

        tree_item_list.insert(2, base_dict)

      #if visit_obj:
        #data['items'][1]['children'] = []
        #children_list  = data['items'][1]['children']
        #for visit in visit_obj:
          #dict_to_append = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
          #dict_to_append['name']    = visit.visit_date.date().isoformat() + "("+ visit.op_surgeon.__unicode__() +")"
          #dict_to_append['id']      = "VISIT_"+ unicode(visit.id)
          #dict_to_append['absoluteUrl'] = visit.get_absolute_url()
          #dict_to_append['editUrl']     = visit.get_edit_url()
          #dict_to_append['delUrl']      = visit.get_del_url()
          #children_list.append(dict_to_append)
      json = simplejson.dumps(data)
      print json
      return HttpResponse(json, content_type = "application/json")
  else:
     raise Http404("Bad Request")

@login_required
def render_visit_list(request):
    '''
    View for Generating Visit List
    Takes on Request Object as argument.
    '''
    user = request.user
    keys = ["sort( date_of_visit)", "sort(-date_of_visit)","sort(+date_of_visit)",
            "sort( op_surgeon)", "sort(-op_surgeon)", "sort(+op_surgeon)",
            ]
    key_sort_map = {
    "sort(+date_of_visit)": "visit_date",
    "sort( date_of_visit)": "visit_date",
    "sort(-date_of_visit)": "-visit_date",
    "sort(+op_surgeon)"       : "op_surgeon",
    "sort( op_surgeon)"       : "op_surgeon",
    "sort(-op_surgeon)"       : "-op_surgeon",
    }
    for key in request.GET:
      if key in keys:
        sort = key_sort_map[key]
        all_visits = VisitDetail.objects.all().order_by(sort)
      else:
        all_visits = VisitDetail.objects.all().order_by('-visit_date')
    data         = []
    for visit in all_visits:
      data_to_append = {}
      data_to_append['id']         = visit.id
      data_to_append['date_of_visit']   = visit.visit_date.strftime("%d/%m/%Y %H:%M:%S")
      data_to_append['surgeon']    = visit.op_surgeon.__unicode__()
      data_to_append['patient_hospital_id']   = visit.patient_detail.patient_hospital_id
      data_to_append['patient']    = visit.patient_detail.__unicode__()
      data_to_append['age']        = visit.patient_detail.age
      data_to_append['sex']        = visit.patient_detail.sex
      data_to_append['active']     = visit.is_active
      data_to_append['del']        = visit.get_edit_url()
      data_to_append['edit']       = visit.get_del_url()
      data.append(data_to_append)
    json = simplejson.dumps(data)
    print json
    return HttpResponse(json, content_type = "application/json")

################################################################################

def get_visit_related_obj_urls(request,id=None):
  """ Receives request and generates URLS for adding/editing a particular 
      VisitDetail and its related Objects (VisitComplaint, VisitHPI, VisitROS). 

      If a VisitDetail has no corresponding related object it returns its addUrl else 
      its editUrl. If like in case of VisitComplaint object it returns a list, 
      the aggregated URL is sent as List.

      if a VisitDetail itsels DoesNotExist, it returns a success=False in JSON.
      
      This is needed for other chained AJAX requests to populate HTML into
      DIV tags in visit/base_add.html or visit/base_edit.html templates
      This return a JSON for the use of calling an AJAX
  """
  
  print "Returning URL for Visit Related Objected with Visit ID of : " + str(id)
  user = request.user
  success = False
  error_message = "No Visits Recorded"
  data = {'visitDetailUrl':'',
          'visitComplaintUrl':'',
          'visitHPIUrl':'',
          'visitROSUrl':''
          }  
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      visit_detail_obj = VisitDetail.objects.get(pk = id)
      visit_complaint_obj = VisitComplaint.objects.filter(visit_detail = visit_detail_obj)
      visit_hpi_obj = VisitHPI.objects.filter(visit_detail = visit_detail_obj)
      visit_ros_obj = VisitROS.objects.filter(visit_detail = visit_detail_obj)      
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      json = simplejson.dumps(data)
      return render_to_response('application/json',json)


    json = simplejson.dumps(data)
    return render_to_response('application/json',json)

  else:
    raise Http404(" Error ! Unsupported Request..")



def visit_add(request,id=None):
  """ Receives request to Add VisitDetail, VisitComplaints, 
      VisitHPI, VisitROS and Physical Examination and routes it
  """
  pass

def visit_edit(request,id=None):
  """ Receives request to Edit VisitDetail, VisitComplaints, 
      VisitHPI, VisitROS and Physical Examination and routes it
  """
  pass

def visit_del(request,id=None):
  """ Receives request to Edit VisitDetail, VisitComplaints, 
      VisitHPI, VisitROS and Physical Examination and routes it
  """
  pass

################################################################################

@login_required
def visit_detail_list(request, id):
  print "Listing Visit Detail for patient with ID: " + str(id)
  user = request.user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      patient_detail_obj = PatientDetail.objects.get(pk = id)
      visit_detail_obj   = VisitDetail.objects.filter(patient_detail = patient_detail_obj).order_by('-visit_date')
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (PatientDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    visit_form_list = []
    if visit_detail_obj:
      error_message = None
      for visit in visit_detail_obj:
#        visit_list = []
        visit_form_list.append([VisitDetailForm(instance = visit), visit])
#        visit_form_list.append(visit_list)
    else:
      error_message = "No Visits Recorded"
    variable = RequestContext(request, {'user'               : user              ,
                                        'visit_detail_obj'   : visit_detail_obj  ,
                                        'visit_form_list'    : visit_form_list   ,
                                        'patient_detail_obj' : patient_detail_obj,
                                        'error_message'      : error_message
                                        })
    return render_to_response('visit/detail/list.html', variable)
  else:
    raise Http404(" Error ! Unsupported Request..")


def format_ros(ros_obj):
    print "Formatting ROS"
    ros_str  = ''
    ros_list = [
                ros_obj.const_symp , 
                ros_obj.eye_symp   , 
                ros_obj.ent_symp   , 
                ros_obj.resp_symp  , 
                ros_obj.gi_symp    , 
                ros_obj.gu_symp    ,
                ros_obj.ms_symp    ,
                ros_obj.integ_symp ,
                ros_obj.psych_symp ,
                ros_obj.endocr_symp, 
                ros_obj.hemat_symp , 
                ros_obj.immuno_symp
               ]
    
    not_nil_count = 0
    for obj in ros_list:
      if obj != 'Nil':
        not_nil_count += 1
        ros_str += obj.capitalize() +'\n'

    if not_nil_count == 0:
      return "NAD"
    else:
      return ros_str


@login_required
def visit_summary(request, id):
  print "Listing Summary for patient with ID: " + str(id)
  user = request.user

  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      patient_detail_obj = PatientDetail.objects.get(pk = id)
      visit_detail_obj   = VisitDetail.objects.filter(patient_detail = patient_detail_obj).order_by('-visit_date')
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (PatientDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
  
    visit_obj_list=[]
    if visit_detail_obj:
      error_message = "Listing the Visits"
      for visit in visit_detail_obj:
        dict_to_append      = {}
        visit_complaint_obj = VisitComplaint.objects.filter(visit_detail = visit)
        visit_hpi_obj       = VisitHPI.objects.filter(visit_detail = visit)
        visit_ros_obj       = VisitROS.objects.filter(visit_detail = visit)
        if visit_ros_obj:
          visit_ros_obj = visit_ros_obj[0]
        dict_to_append[visit] = {'complaint': visit_complaint_obj,
                                 'hpi'      : visit_hpi_obj,
                                 'ros'      : format_ros(visit_ros_obj)
                                }
        visit_obj_list.append(dict_to_append)
    else:
      error_message = "No Visits Recorded"
    variable = RequestContext(request, {'user'               : user              ,
                                        'visit_detail_obj'   : visit_detail_obj  ,
                                        'visit_obj_list'     : visit_obj_list    ,
                                        'patient_detail_obj' : patient_detail_obj,
                                        'error_message'      : error_message
                                        })
    return render_to_response('visit/summary.html', variable)
  else:
    raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_detail_add(request,  id, nature = 'initial'):
  """ Adds a new VisitDetail Object and related Objects: VisitComplaint,VisitROS, VisitHPI
      Takes request and id of PatientDetail object
      the nature of visit is defaulted to 'initial'.
      Implementation of separate visits for 'initial' , 'fu' etc.. can be implemented later.
  """
  print "Received request to add VisitDetail"
  print "Request nature is: ", request.method

  user = request.user
  success = False
  error_message= None
  form_errors=[]

  try:
    id = int(id)
    patient_detail_obj  = PatientDetail.objects.get(pk = id)
    print "Patient is: ", patient_detail_obj
    visit_detail_objs   = VisitDetail.objects.filter(patient_detail = patient_detail_obj).filter(is_active = True)
  except (TypeError, NameError, ValueError, AttributeError, KeyError):
    raise Http404("Error ! Invalid Request Parameters. ")
  except (PatientDetail.DoesNotExist):
    raise Http404("Requested Patient Does not exist.")
  
  if not patient_detail_obj.can_add_new_visit():
    error_message = '''Cannot add new visit now. 
                        There may be a active admission / visit. 
                        Please close that and try again
                    '''
    print error_message
    raise Http404(error_message)
  
  else:
    print patient_detail_obj, " can add VisitDetail"
    visit_detail_obj = VisitDetail(patient_detail = patient_detail_obj)
    visit_complaint_obj = VisitComplaint(visit_detail = visit_detail_obj)
    visit_hpi_obj       = VisitHPI(visit_detail = visit_detail_obj)
    visit_ros_obj       = VisitROS(visit_detail = visit_detail_obj)
    VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm, can_delete=True, can_order=True)        
    complaint_add_icon_html      = complaint_add_icon_template.render(RequestContext(request,{'user':user}))
    complaint_remove_icon_html  = complaint_remove_icon_template.render(RequestContext(request,{'user':user}))
    form_auto_id = "id_%s"+"_new_visit_"+ str(id)
    total_form_auto_id = "id_form-TOTAL_FORMS_new_visit_"+str(id)

    if request.method == "GET" and request.is_ajax():

      if nature == 'initial':
        print "Adding an Initial Visit for ", patient_detail_obj
        visit_detail_form    = VisitDetailForm(instance = visit_detail_obj, 
                                               auto_id  = "id_new_visit_detail"+ str(id)+"_%s")
        #visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj,
                                                  #auto_id  = "id_new_visit_complaint"+ str(id)+"_%s")
        visit_complaint_formset = VisitComplaintFormset(queryset=VisitComplaint.objects.none(),
                                                        auto_id= form_auto_id)
        #visit_complaint_form_html = visit_complaint_add(request,id=id)
        visit_hpi_form       = VisitHPIForm(instance = visit_hpi_obj,
                                            auto_id  = "id_new_visit_hpi"+ str(id)+"_%s")
        visit_ros_form       = VisitROSForm(instance = visit_ros_obj,
                                            auto_id  = "id_new_visit_ros"+ str(id)+"_%s")
        variable = RequestContext(request, {'user'                     : user                  ,
                                            'visit_detail_obj'         : visit_detail_obj      ,
                                            'visit_detail_form'        : visit_detail_form     ,
                                            'visit_complaint_formset'  : visit_complaint_formset  ,
                                            #'visit_complaint_form_html'     : visit_complaint_form_html,
                                            'visit_hpi_form'           : visit_hpi_form        ,
                                            'visit_ros_form'           : visit_ros_form        ,
                                            'patient_detail_obj'       : patient_detail_obj    ,
                                            'error_message'            : error_message         ,
                                            'complaint_add_icon_html'  : complaint_add_icon_html,
                                            'complaint_remove_icon_html':complaint_remove_icon_html,
                                            'success'                  : success,
                                            'form_auto_id'             : form_auto_id,
                                            'total_form_auto_id'       : total_form_auto_id
                                            })
        return render_to_response('visit/detail/add.html', variable)

      elif nature == 'fu':
        #TODO
        pass

    elif request.method == "POST" and request.is_ajax():
      print "Received request to add visit..."
      print "POST Request Contains::"
      print request.POST
      visit_detail_form    = VisitDetailForm(request.POST, instance = visit_detail_obj)
      #visit_complaint_form = VisitComplaintForm(request.POST, instance = visit_complaint_obj)
      #VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)              
      visit_complaint_formset = VisitComplaintFormset(request.POST,auto_id= form_auto_id)
      visit_hpi_form       = VisitHPIForm(request.POST, instance = visit_hpi_obj)
      visit_ros_form       = VisitROSForm(request.POST, instance = visit_ros_obj)

      if visit_detail_form.is_valid()       and \
        visit_complaint_formset.is_valid() and \
        visit_hpi_form.is_valid()          and \
        visit_ros_form.is_valid():
        
        saved_visit     = visit_detail_form.save()
        saved_visit_complaints = visit_complaint_formset.save(commit=False)
        print "Saved visit is:"
        print saved_visit
        print saved_visit_complaints
        for complaint in saved_visit_complaints:
          print "Saving Complaints..."
          print complaint
          complaint.visit_detail = saved_visit
          complaint.save()

        saved_visit_hpi = visit_hpi_form.save(commit=False)
        saved_visit_hpi.visit_detail = saved_visit
        saved_visit_hpi.save()
        saved_visit_ros = visit_ros_form.save(commit=False)
        saved_visit_ros.visit_detail = saved_visit
        saved_visit_ros.save()
        success       = True
        error_message = "Visit Added Successfully"

      else:
        success       = False
        error_message = '''Error! Visit Could not be added. 
                          Please check the forms for errors
                        '''
      data = { 'success'       : success      ,
              'error_message' : error_message
            }
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')

    else:
      raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_detail_edit(request, id):
  user = request.user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      visit_detail_obj      = VisitDetail.objects.get(pk = id)
      visit_complaint_obj   = VisitComplaint.objects.filter(visit_detail = visit_detail_obj)
      visit_hpi_obj         = VisitHPI.objects.filter(visit_detail = visit_detail_obj)
      visit_ros_obj         = VisitROS.objects.filter(visit_detail = visit_detail_obj)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    error_message = None
    form_field_auto_id = 'id_edit_visit_detail_'+str(id)
    visit_detail_form = VisitDetailForm(instance = visit_detail_obj, auto_id= form_field_auto_id+"_%s")

    complaint_formset_auto_id = "id_%s"+"_edit_visit_complaint_"+ str(id)
    complaint_total_form_auto_id = "id_form-TOTAL_FORMS_edit_visit_complaint_"+str(id)
    VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)        
    visit_complaint_formset = VisitComplaintFormset(queryset = VisitComplaint.objects.filter(visit_detail = visit_detail_obj),
                                                    auto_id=complaint_formset_auto_id
                                                    )
    complaint_count = len(visit_complaint_obj)
    complaint_add_icon_template     = get_template('visit/snippets/icons/complaints_add.html')
    complaint_remove_icon_template = get_template('visit/snippets/icons/complaints_remove.html')
    complaint_add_icon_html      = complaint_add_icon_template.render(RequestContext(request,{'user':user}))
    complaint_remove_icon_html  = complaint_remove_icon_template.render(RequestContext(request,{'user':user}))


    #if visit_complaint_obj:
      #visit_complaint_obj = visit_complaint_obj[0]
      #c_auto_id = 'id_edit_visit_complaint_'+str(visit_complaint_obj.id)
      #visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj, auto_id = c_auto_id +"_%s")
    #else:
      #visit_complaint_form = None
      #visit_complaint_formset  = None
    
    if visit_hpi_obj:
      visit_hpi_obj = visit_hpi_obj[0]
      h_auto_id = 'id_edit_visit_hpi_'+ str(visit_hpi_obj.id)
      visit_hpi_form = VisitHPIForm(instance = visit_hpi_obj, auto_id = h_auto_id+"_%s")
    else:
      visit_hpi_form = None
    
    if visit_ros_obj:
      visit_ros_obj = visit_ros_obj[0]
      r_auto_id     = 'id_edit_visit_ros_' + str(visit_ros_obj.id)
      visit_ros_form = VisitROSForm(instance = visit_ros_obj, auto_id= r_auto_id+"_%s")
    else:
      visit_ros_form = None

    variable = RequestContext(request, {'user'                  : user                  ,
                                        'visit_detail_obj'      : visit_detail_obj      ,
                                        'visit_detail_form'     : visit_detail_form     ,
                                        #'visit_complaint_form'  : visit_complaint_form  ,
                                        'visit_complaint_formset': visit_complaint_formset,
                                        'complaint_count'       : complaint_count,
                                        'visit_hpi_form'       : visit_hpi_form        ,
                                        'visit_ros_form'       : visit_ros_form        ,
                                        'patient_detail_obj'    : visit_detail_obj.patient_detail   ,
                                        'error_message'         : error_message         ,
                                        'complaint_add_icon_html': complaint_add_icon_html,
                                        'complaint_remove_icon_html': complaint_remove_icon_html,
                                        'complaint_formset_auto_id':complaint_formset_auto_id,
                                        'complaint_total_form_auto_id': complaint_total_form_auto_id
                                        })
    return render_to_response('visit/detail/edit.html', variable)

  if request.method == "POST" and request.is_ajax():
    try:
      id                  = int(id)
      visit_detail_obj    = VisitDetail.objects.get(pk = id)
      visit_complaint_obj = VisitComplaint.objects.filter(visit_detail = visit_detail_obj)
      visit_hpi_obj       = VisitHPI.objects.filter(visit_detail = visit_detail_obj)
      visit_ros_obj       = VisitROS.objects.filter(visit_detail = visit_detail_obj)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Visit Does not exist.")
    success                = False
    error_message          = None

    if visit_complaint_obj and visit_hpi_obj and visit_ros_obj:
      visit_detail_edit_form = VisitDetailForm(request.POST, instance = visit_detail_obj)
      #visit_complaint_form   = VisitComplaintForm(request.POST, instance = visit_complaint_obj[0])
      complaint_formset_auto_id = "id_%s"+"_edit_visit_complaint_"+ str(id)
      complaint_total_form_auto_id = "id_form-TOTAL_FORMS_edit_visit_complaint_"+str(id)      
      VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)
      visit_complaint_formset = VisitComplaintFormset(request.POST,
                                                      queryset = visit_complaint_obj,
                                                      auto_id= complaint_formset_auto_id
                                                      )

      visit_hpi_form         = VisitHPIForm(request.POST, instance = visit_hpi_obj[0])
      visit_ros_form         = VisitROSForm(request.POST, instance = visit_ros_obj[0])
      
      if visit_detail_edit_form.is_valid() and \
        visit_complaint_formset.is_valid()   and \
        visit_hpi_form.is_valid()         and \
        visit_ros_form.is_valid():

        saved_visit   = visit_detail_edit_form.save()
        saved_visit_complaint = visit_complaint_formset.save(commit = False)

        for complaint in saved_visit_complaint:
          complaint.visit_detail = saved_visit
          saved_complaint = complaint.save()
          print saved_complaint

        #saved_visit_complaint.visit_detail = saved_visit
        #saved_visit_complaint.save()

        saved_visit_hpi = visit_hpi_form.save(commit = False)
        saved_visit_hpi.visit_detail = saved_visit
        saved_visit_hpi.save()

        saved_visit_ros = visit_ros_form.save(commit = False)
        saved_visit_ros.visit_detail = saved_visit
        saved_visit_ros.save()

        #saved_visit.visit_status_change(unicode(saved_visit.status))

        success       = True
        error_message = "Visit Edited Successfully"
      else:
        success       = False
        
        #def form_error_formatter(error_list):
          #error_string = ''
          #if error_list:
            #for error in error_list:
              #error_string_to_join    = error + "\n"
              #error_string += error_string_to_join
            #return error_string
          #else:
            #return ''

        #visit_detail_form_error    = form_error_formatter(visit_detail_edit_form.errors)
        ##visit_complaint_form_error = form_error_formatter(visit_complaint_form.errors)
        #visit_hpi_form_error       = form_error_formatter(visit_hpi_form.errors)
        #visit_ros_form_error       = form_error_formatter(visit_ros_form.errors)

        #error_message = "Error! Visit Could not be edited" + "\n" +\
                        #visit_detail_form_error    + "\n" + \
                        ##visit_complaint_form_error + "\n" + \
                        #visit_hpi_form_error       + "\n" + \
                        #visit_ros_form_error       + "\n" 

      data = { 'success'      : success      ,
              'error_message': None
            }
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("ERROR!  The visit has not associated complaints, HPI or ROS to edit")
  else:
    raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_detail_del(request, id):
  if request.method == "GET" and request.is_ajax():
    user = request.user
    if user.has_perm('visit.delete_visitdetail'):
        try:
          id = int(id)
          visit_detail_obj = VisitDetail.objects.get(pk = id)
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
          raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
          raise Http404("Requested Patient Does not exist.")
        error_message = None
        visit_detail_obj.delete()
        success = True
        error_message = "Successfully Deleted Visit."
        data = {'success': success, 'error_message': error_message}
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type = 'application/json')
    else:
      success = False
      error_message = "Insufficient Permission. Could not delete."
      data = {'success': success, 'error_message': error_message}
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_detail_close(request, id):
  if request.method == "GET" and request.is_ajax():
    user = request.user
    if user.has_perm('visit.change_visitdetail'):
      try:
        id = int(id)
        visit_detail_obj = VisitDetail.objects.get(pk = id)
      except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")
      except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")
      #visit_detail_obj._close_all_active_visits()
      visit_detail_obj._close_visit()
      error_message = None
      success       = True
      error_message = "Successfully Deleted Visit."
      data          = {'success': success, 'error_message': error_message}
      json          = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      success       = False
      error_message = "Insufficient Permissions to Change Visit"
      data          = {'success': success, 'error_message': error_message}
      json          = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_follow_up_add(request, id):

  user = request.user
  print "Received Request to add a follow up visit from ", user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      visit_detail_obj  = VisitDetail.objects.get(pk = id)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Visit Does not exist.")
    except(visit_detail_obj.is_active == False):
      raise Http404("The Visit is Closed. Cannot add Followup Visits")

    visit_follow_up_obj = VisitFollowUp(visit_detail = visit_detail_obj)
    visit_follow_up_form = VisitFollowUpForm(instance = visit_follow_up_obj, 
                                             auto_id  = 'id_visit_follow_up_'+ str(visit_detail_obj.id)+"_%s"
                                             )
    variable = RequestContext(request, {'user'                  : user                  ,
                                        'visit_detail_obj'      : visit_detail_obj      ,
                                        'visit_follow_up_obj'   : visit_follow_up_obj   ,
                                        'visit_follow_up_form'  : visit_follow_up_form  ,
                                        'patient_detail_obj'    : visit_detail_obj.patient_detail    
                                        })
    return render_to_response('visit/follow_up/add.html', variable)

  if request.method == "POST" and request.is_ajax():
    print "Received request to add a Follow-Up OPD Visit..."
    try:
      id                = int(id)
      visit_detail_obj  = VisitDetail.objects.get(pk = id)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Visit Does not exist.")

    visit_follow_up_obj  = VisitFollowUp(visit_detail  = visit_detail_obj)
    visit_follow_up_form = VisitFollowUpForm(request.POST, instance = visit_follow_up_obj)

    if visit_follow_up_form.is_valid():
       saved_follow_up = visit_follow_up_form.save()
       success         = True
       error_message   = "Follow Up Visit Added Successfully"
    else:
      success = False
      error_message = "Error! Follow-up visit Could not be added"
    data = { 'success'       : success      ,
             'error_message' : error_message
           }
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_follow_up_edit(request, id):

  user = request.user
  print "Received Request to add a follow up visit from ", user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      visit_follow_up_obj  = VisitFollowUp.objects.get(pk = id)
      visit_detail_obj     = visit_follow_up_obj.visit_detail
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitFollowUp.DoesNotExist):
      raise Http404("Requested Visit Does not exist.")
    except(visit_follow_up_obj.visit_detail.is_active == False):
      raise Http404("The Visit is Closed. Cannot add Followup Visits")

    visit_follow_up_form = VisitFollowUpForm(instance = visit_follow_up_obj, 
                                             auto_id  = 'id_visit_follow_up_'+ str(visit_follow_up_obj.id)+"_%s"
                                             )
    variable = RequestContext(request, {'user'                  : user                  ,
                                        'visit_detail_obj'      : visit_detail_obj      ,
                                        'visit_follow_up_obj'   : visit_follow_up_obj   ,
                                        'visit_follow_up_form'  : visit_follow_up_form  ,
                                        'patient_detail_obj'    : visit_detail_obj.patient_detail    
                                        })
    return render_to_response('visit/follow_up/edit.html', variable)

  if request.method == "POST" and request.is_ajax():
    print "Received request to add a Follow-Up OPD Visit..."
    try:
      id = int(id)
      visit_follow_up_obj  = VisitFollowUp.objects.get(pk = id)
      visit_detail_obj     = visit_follow_up_obj.visit_detail
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitFollowUp.DoesNotExist):
      raise Http404("Requested Visit Does not exist.")
    except(visit_follow_up_obj.visit_detail.is_active == False):
      raise Http404("The Visit is Closed. Cannot add Followup Visits")
    
    visit_follow_up_form = VisitFollowUpForm(request.POST, instance = visit_follow_up_obj)

    if visit_follow_up_form.is_valid():
       saved_follow_up = visit_follow_up_form.save()
       success = True
       error_message = "Follow Up Visit Edited Successfully"
    else:
      success = False
      error_message = "Error! Follow-up visit Could not be added"
    data = { 'success'       : success      ,
             'error_message' : error_message
           }
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_follow_up_del(request, id):

  user = request.user
  print "Received Request to add a follow up visit from ", user
  if request.method == "GET" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")


################################################################################

@login_required
def visit_complaint_add(request,id=None):
  user = request.user
  success = False
  error_message = "Complaint Added Successfully"
  form_errors   = []  
  try:
    id = int(id)
    visit_detail_obj  = VisitDetail.objects.get(pk = id)
    patient_detail_obj = visit_detail_obj.patient_detail
    visit_complaint_objs = VisitComplaint.objects.filter(visit_detail = visit_detail_obj)
    visit_complaint_obj = VisitComplaint(visit_detail = visit_detail_obj)  
    VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm,extra=1)
  except (TypeError, NameError, ValueError, AttributeError, KeyError):
    raise Http404("Error ! Invalid Request Parameters. ")
  except (VisitDetail.DoesNotExist):
    raise Http404("Requested Visit Does not exist.")    

  if request.method == "GET" and request.is_ajax():
    print "Received GET request to add Visit Complaints "
  #visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj,
                                              #auto_id  = "id_new_visit_complaint"+ str(id)+"_%s")
    visit_complaint_formset = VisitComplaintFormset(queryset = visit_complaint_objs)
    print visit_complaint_formset
    variable = RequestContext(request, {'user'                     : user                  ,
                                        'visit_detail_obj'         : visit_detail_obj      ,
                                        'visit_complaint_formset'  : visit_complaint_formset  ,
                                        'patient_detail_obj'       : patient_detail_obj    
                                       })
    return render_to_response('visit/complaints/add.html', variable)

  if request.method == "POST" and request.is_ajax():
    print "Received POST request to add Visit complaints ..."
    #visit_complaint_form = VisitComplaintForm(request.POST, instance = visit_complaint_obj)
    visit_complaint_formset = VisitComplaintFormset(request.POST)

    if visit_complaint_formset.is_valid():
      saved_visit_complaint = visit_complaint_formset.save(commit=False)
      for complaint in saved_visit_complaint:
        complaint.visit_detail = saved_visit
        complaint.save()

      success       = True
    else:
      success       = False
      error_message = '''Error! Complaint Could not be added. 
                          Please check the forms for errors
                      '''
    data = { 'success'       : success      ,
             'error_message' : error_message
           }
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_complaint_edit(request,id=None):
  pass

@login_required
def visit_complaint_del(request,id=None):
  if request.method == "GET" and request.is_ajax():
    user = request.user
    if user.has_perm('visit.delete_visitcomplaint'):
        try:
          id = int(id)
          visit_complaint_obj = VisitComplaint.objects.get(pk = id)
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
          raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitComplaint.DoesNotExist):
          raise Http404("Requested Complaint Does not exist.")
        error_message = None
        visit_complaint_obj.delete()
        success = True
        error_message = "Successfully Deleted Visit Complaint"
        data = {'success': success, 'error_message': error_message}
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type = 'application/json')
    else:
      success = False
      error_message = "Insufficient Permission. Could not delete."
      data = {'success': success, 'error_message': error_message}
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")


################################################################################

@login_required
def visit_status_list(request,id):
  user = request.user
  try:
   id = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

@login_required
def visit_status_edit(request, id):
  user = request.user
  try:
   id = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

################################################################################

@login_required
def visit_nature_list(request,id):
  user = request.user
  try:
   id = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

@login_required
def visit_nature_edit(request, id):
  user = request.user
  try:
   id        = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

################################################################################

@login_required
def visit_close(request, id):
  user = request.user
  if user.is_staff:
    try:
     id        = int(id)
     visit_obj = VisitDetail.objects.get(pk = id)
    except (NameError, ValueError, AttributeError, KeyError):
     raise Http404("Bad Request:: Invalid Request Parameters")
    except (VisitDetail.DoesNotExist):
     raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
    if request.method=="GET" and request.is_ajax():
      visit_obj.visit_status_change('discharged')
      success       = True
      error_message = "Visit Closed Successfully"
      data = {"success": success, 'error_message': error_message}
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404(" Error ! Unsupported Request..")
  else:
    raise Http404(" Error ! Permission Denied..")

################################################################################





################################################################################


#@login_required
#def visit_action(request,action = 'add', id = 'id'):
#  if request.user:
#    user = request.user
#    if action == "add":
#      if request.method == "GET":
# try:
#   id = int(id)
#   pat_obj = PatientDetail.objects.get(pk = id)
# except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
#   raise Http404("Bad Request: Raised ValueError / TypeError / PatientDetail DoesNotExist")
# visit_objs    = VisitDetail.objects.filter(patient_detail = pat_obj)
# adm_obj       = Admission.objects.filter(patient_detail = pat_obj).filter(admission_closed = False)
# active_visits = []
# if visit_objs:
#   for visits in visit_objs:
#     active_visits = VisitStatus.objects.filter(visit_detail = visits).filter(is_active = True)
# if active_visits:
#   error_message = "Patient has an active Visit. You cannot add further visits for the same patient"
#   #variable     = RequestContext(request, {'user':user, 'error_message':error_message})
#   return HttpResponse(error_message)
# elif adm_obj:
#   error_message = "Patient has an active Admission. You cannot add OPD notes for the same patient"
#   return HttpResponse(error_message)
# else:
#   visit_detail_obj      = VisitDetail(patient_detail = pat_obj)
#   visit_status_obj      = VisitStatus(visit_detail = visit_detail_obj)
#   visit_complaint_obj   = VisitComplaints(visit_detail = visit_detail_obj)
#   visit_nature_obj      = VisitNature(visit_detail = visit_detail_obj)
#
#   visit_detail_form           = VisitDetailForm(instance = visit_detail_obj)
#   visit_nature_form           = VisitNatureForm(instance = visit_nature_obj)
#   visit_status_form           = VisitStatusForm(instance = visit_status_obj)
#   visit_complaint_form        = VisitComplaintsForm(instance = visit_complaint_obj)
#
#   action = '/visit/add/'+str(pat_obj.id) +'/'
#   method = 'post'
#   button = 'Add Visit'
#   variable = RequestContext(request, {'user':user,
#               'pat_obj':pat_obj,
#               'active':active_visits,
#               'visit_detail_obj':visit_detail_obj,
#               'visit_status_obj':visit_status_obj,
#               'visit_nature_obj':visit_nature_obj,
#               'visit_complaint_obj':visit_complaint_obj,
#
#               'visit_detail_form':visit_detail_form,
#               'visit_nature_form':visit_nature_form,
#               'visit_status_form':visit_status_form,
#               'visit_complaint_form':visit_complaint_form,
#
#               'action':action,
#               'method':method,
#               'button':button,
#               })
#   return render_to_response('visit/visit_actions.html', variable)
#
#      elif request.method == "POST":
# try:
#   id = int(id)
#   pat_obj = PatientDetail.objects.get(pk = id)
# except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
#   raise Http404("Bad Request: Raised ValueError / TypeError / PatientDetail DoesNotExist")
# adm_obj = Admission.objects.filter(patient_detail = pat_obj).filter(admission_closed = False)
# if adm_obj:
#   error_message = "Patient has an active Admission.\nYou cannot add OPD notes for the same patient"
#   return HttpResponseRedirect('/phy_exam/home/'+str(adm_obj.id)+'/')
# else:
#   visit_detail_obj    = VisitDetail(patient_detail = pat_obj)
#   visit_status_obj    = VisitStatus(visit_detail = visit_detail_obj)
#   #visit_complaint_obj    = VisitComplaints(visit_detail = visit_detail_obj)
#   visit_nature_obj    = VisitNature(visit_detail = visit_detail_obj)
#
#   visit_detail_form         = VisitDetailForm(request.POST, instance = visit_detail_obj)
#   visit_nature_form           = VisitNatureForm(request.POST,instance = visit_nature_obj)
#   visit_status_form           = VisitStatusForm(request.POST,instance = visit_status_obj)
#   #visit_complaint_form        = VisitComplaintsForm(request.POST,instance = visit_complaint_obj)
#
#   if visit_detail_form.is_valid()and visit_nature_form.is_valid()and visit_status_form.is_valid():
#      visit_detail_obj  = visit_detail_form.save()
#      visit_detail_obj.patient_detail = pat_obj
#      visit_detail_obj.save()
#
#      #visit_nature_form.cleaned_data['visit_detail'] = visit_detail_obj
#      visit_nature_obj.visit_detail = visit_detail_obj
#      visit_nature_obj = visit_nature_form.save()
#      visit_nature_obj.save()

#      #visit_status_form.cleaned_data['visit_detail'] = visit_detail_obj
#      visit_status_obj.visit_detail = visit_detail_obj
#      visit_status_obj = visit_status_form.save()

#      if visit_status_form.cleaned_data['status'] == 'admission' or visit_status_form.cleaned_data['status'] =='discharge':
#        visit_status_obj.is_active = 'False'
#      else:
#        visit_status_obj.is_active = 'True'
#      visit_status_obj.save()

#      error_message        = "Visit Details saved Successfully"
#      visit_complaints_formset = VisitComplaintsFormset(queryset = VisitComplaints.objects.filter(visit_detail = visit_detail_obj))
#      action               = 'visit/complaints/add/'+str(visit_detail_obj.id)+'/'
#      method               = 'post'
#      button               = 'Add Complaints'
#      variable             = RequestContext(request, {'user':user,
#            'visit_detail_obj':visit_detail_obj,
#            'visit_complaints_formset':visit_complaints_formset,
#            'method':method,
#            'action':action,
#            'button':button,
#            'error_message':error_message
#            })
#      return render_to_response('visit/visit_complaints.html', variable)
#      #return HttpResponseRedirect('/visit/list/')
#   else:
#     action   = '/visit/add/'+str(pat_obj.id) +'/'
#     method   = 'post'
#     button   = 'Resubmit'
#     variable = RequestContext(request, {'user':user,
#           'pat_obj':pat_obj,
#
#           'visit_detail_obj':visit_detail_obj,
#           'visit_status_obj':visit_status_obj,
#           'visit_nature_obj':visit_nature_obj,
#           #'visit_complaint_obj':visit_complaint_obj,
#
#           'visit_detail_form':visit_detail_form,
#           'visit_nature_form':visit_nature_form,
#           'visit_status_form':visit_status_form,
#           #'visit_complaint_formset':visit_complaint_formset,

#           'action':action,
#           'method':method,
#           'button':button,
#           })
#     return render_to_response('visit/visit_actions.html', variable)
#      else:
# return Http404("Bad Request")
#    elif action == 'edit':
#      pass
#    elif action == 'del':
#      pass
#    else:
#      raise Http404("Unknown Action:: " +str(action))
#  else:
#    return HttpResponseRedirect('/login/')

#@login_required
#def visit_complaints(request, id):
#  global TOTAL_COMPLAINTS_FORM
#  if request.user:
#    user = request.user
#    if request.method == 'POST':
#      try:
# id = int(id)
# visit_detail_obj = VisitDetail.objects.get(pk = id)
#      except (TypeError, ValueError, AttributeError, VisitDetail.DoesNotExist):
# raise Http404("Error !!:: Type / AttributeError / ValueError/ DoesNotExist Error ")
#      visit_complaints_obj  = VisitComplaints(visit_detail = visit_detail_obj)
#      visit_complaints_formset = VisitComplaintsFormset(request.POST)
#      if visit_complaints_formset.is_valid():
#        instances = visit_complaints_formset.save(commit = False)
#        for instance in instances:
#     instance.visit_detail = visit_detail_obj
#     instance.save()
#        if 'add_more_complaints' in request.POST:
#   TOTAL_COMPLAINTS_FORM  = int(request.POST['form-TOTAL_FORMS'])+1
#   visit_complaints_formset = VisitComplaintsFormset(queryset = VisitComplaints.objects.filter(visit_detail = visit_detail_obj))
#   action               = 'visit/complaints/add/'+str(visit_detail_obj.id)+'/'
#   method               = 'post'
#   button               = 'Add Complaints'
#   error_message = "Complaints have been saved.\nYou can add "+ str(10-TOTAL_COMPLAINTS_FORM) +" more complaints."
#   max_forms_reached = False
#   if TOTAL_COMPLAINTS_FORM == 10:
#         error_message = "Cannot add more complaints"
#         max_forms_reached = True
#   variable = RequestContext(request, {'user':user,
#                 'visit_detail_obj':visit_detail_obj,
#                 'visit_complaints_formset':visit_complaints_formset,
#                 'action':action,
#                 'button':button,
#                 'method':method,
#                 'error_message':error_message,
#                 'max_forms_reached':max_forms_reached,
#                 })
#   return render_to_response('visit/visit_complaints.html', variable)
# else:
#   return HttpResponseRedirect('/visit/list')
#      else:
# visit_action(request, action = 'add', id = id)

@login_required
def visit_home(request, id = id):
  if request.user:
    user = request.user
    try:
      id = int(id)
      visit_obj = VisitDetail.objects.get(pk = id)
    except(ValueError, AttributeError, TypeError, VisitDetail.DoesNotExist):
      raise Http404('Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
    pat_detail_obj       = visit_obj.patient_detail
#    visit_status_obj     = VisitStatus.objects.filter(visit_detail = visit_obj)
#    visit_nature_obj     = VisitNature.objects.filter(visit_detail = visit_obj)
#    visit_complaints_obj = VisitComplaints.objects.filter(visit_detail = visit_obj)
    #phy_exam_obj      = PhyExam.objects.filter(visit_detail = visit_obj)
    #reg_exam_obj      = RegExam.objects.filter(visit_detail = visit_obj)
    if request.method == 'GET':
      variable = RequestContext(request, {'user':user,
            'pat_detail_obj':pat_detail_obj,
            'visit_obj':visit_obj,
#           'visit_status_obj':visit_status_obj,
#           'visit_nature_obj':visit_nature_obj,
#           'visit_complaints_obj':visit_complaints_obj,
            #'phy_exam_obj':phy_exam_obj,
            #'reg_exam_obj':reg_exam_obj,
            })
      return render_to_response('visit/visit_home.html', variable)
    elif request.method == 'POST':
      pass
    else:
      raise Http404("Bad Request.." + str(request.method))
  else:
    return HttpResponseRedirect('/login')


@login_required
def render_visit_pdf(request, id):
  if request.user:
    user = request.user
    try:
      id = int(id)
      visit_detail_obj = VisitDetail.objects.get(pk = id)
    except(ValueError, AttributeError, TypeError, VisitDetail.DoesNotExist):
      raise Http404('Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
    pat_detail_obj       = visit_detail_obj.patient_detail
    if request.method == 'GET':
      variable = RequestContext(request, 
                                {'user'            : user,
                                'pat_detail_obj'  : pat_detail_obj,
                                'visit_detail_obj': visit_detail_obj,
                                }
      )
      return render_to_response('visit/visit_pdf_template.html', variable)
    elif request.method == 'POST':
      pass
    else:
      raise Http404("Bad Request.." + str(request.method))
  else:
    return HttpResponseRedirect('/login')



@login_required
def render_patient_visits_pdf(request, id):
  if request.user:
    user = request.user
    try:
      id             = int(id)
      patient_detail_obj = PatientDetail.objects.get(pk = id)
    except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
      raise Http404('Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
    visit_detail_obj    = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    visit_obj_list=[]


    if visit_detail_obj:
      error_message = "Listing the Visits"
      for visit in visit_detail_obj:
        dict_to_append      = {}
        visit_complaint_obj = VisitComplaint.objects.filter(visit_detail = visit)
        visit_hpi_obj       = VisitHPI.objects.filter(visit_detail = visit)
        visit_ros_obj       = VisitROS.objects.filter(visit_detail = visit)
        if visit_ros_obj:
          visit_ros_obj = visit_ros_obj[0]
        dict_to_append[visit] = {'complaint': visit_complaint_obj,
                                 'hpi'      : visit_hpi_obj,
                                 'ros'      : format_ros(visit_ros_obj)
                                }
        visit_obj_list.append(dict_to_append)
    else:
      error_message = "No Visits Recorded"

    if request.method == 'GET':
      variable = RequestContext(request, {'user'               : user              ,
                                          'visit_detail_obj'   : visit_detail_obj  ,
                                          'visit_obj_list'     : visit_obj_list    ,
                                          'patient_detail_obj' : patient_detail_obj,
                                          'error_message'      : error_message     ,
                                          'pagesize'           : "A4"
                                        })

      template     = get_template('visit/patient_visit_pdf_template.html')
      html         = template.render(variable)
      result       = StringIO.StringIO()
      pdf          = pisa.pisaDocument(StringIO.StringIO( html.encode("UTF-8") ), result)

      if not pdf.err:
          return HttpResponse(result.getvalue(),mimetype='application/pdf')
      return HttpResponse("Error Generating PDF.. %s" %(html) )

    else:
      raise Http404("Bad Request.." + str(request.method))
  else:
    return HttpResponseRedirect('/login')