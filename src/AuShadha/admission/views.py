##--------------------------------------------------------------
# Views for Patient admission and details display and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date: 26-09-2010
##---------------------------------------------------------------


# General Django Imports----------------------------------

from django.shortcuts 							import render_to_response
from django.http 										import Http404, HttpResponse, HttpResponseRedirect
from django.template 								import RequestContext
from django.contrib.auth.models 		import User
from django.contrib.auth.decorators import login_required
from django.core.paginator 					import Paginator
from django.utils                   import simplejson

#from django.views.decorators.csrf 	import csrf_exempt
#from django.core.context_processors import csrf

# General Module imports-----------------------------------
from datetime 											import datetime, date, time


# Application Specific Model Imports-----------------------

import ds.settings

from patient.models 		import *
from surgeon.models		 	import *
from admission.models 	import *
from discharge.models 	import *
from visit.models 			import *
from phyexam.models 		import *
from procedure.models 		import *


@login_required
def get_admission_main_window(request, id):
	'''
	Editing Admission Object.
	Takes id as the argument.
	'''
	if request.user :
		user = request.user
		try:
			id	= int(id)
			adm_obj								= Admission.objects.get(pk = id)
			patient_detail_obj    = adm_obj.patient_detail
			adm_complaint_obj			= AdmissionComplaint.objects.filter(admission_detail = adm_obj)
			adm_hpi_obj						= AdmissionHPI.objects.filter(admission_detail = adm_obj)
			adm_past_history_obj 	= AdmissionPastHistory.objects.filter(admission_detail = adm_obj)
			adm_phy_exam_obj			= PhyExam.objects.filter(admission_detail = adm_obj)
			adm_inv_obj						= AdmissionInv.objects.filter(admission_detail = adm_obj)
			adm_imaging_obj				= AdmissionImaging.objects.filter(admission_detail = adm_obj)
			adm_procedure_obj			= ProcedureDetail.objects.filter(admission_detail = adm_obj)
			adm_discharge_obj			= DischargeDetail.objects.filter(admission_detail = adm_obj)
			variable							= RequestContext(request,{'user'                 : user                , 
																											'adm_obj'              : adm_obj             ,
																											'adm_complaint_obj'    : adm_complaint_obj   ,
																											'adm_hpi_obj'          : adm_hpi_obj         ,
																											'adm_past_history_obj' : adm_past_history_obj,
																											'adm_phy_exam_obj'     : adm_phy_exam_obj    ,
																											'adm_inv_obj'          : adm_inv_obj         ,
																											'adm_imaging_obj'      : adm_imaging_obj     ,
																											'adm_procedure_obj'    : adm_procedure_obj   ,
																											'adm_discharge_obj'    : adm_discharge_obj
																										}
																							)
			return render_to_response('admission/main_window.html',variable)
		except (ValueError,AttributeError,Admission.DoesNotExist, TypeError):
			raise Http404("Bad Request")
	else:
		raise Http404("Please Log in")


@login_required
def get_admission_tree_json(request, id):
	'''
	Creates the Admission Tree in DOJO
	Takes id as the argument.
	'''
	if request.user :
		user = request.user
		if request.method == "GET" and request.is_ajax():
			try:
				admission_id = int(id)
				adm_obj      = Admission.objects.get(pk = admission_id)
			except(TypeError,AttributeError, ValueError, NameError,KeyError):
				raise Http404("Invalid Request Parameters: Please Try Again")
			except(Admission.DoesNotExist):
				raise Http404("ERROR!: No Admission Found !")
			patient_detail_obj    = adm_obj.patient_detail
			adm_complaint_obj			= AdmissionComplaint.objects.filter(admission_detail = adm_obj)
			adm_hpi_obj						= AdmissionHPI.objects.filter(admission_detail = adm_obj)
			adm_past_history_obj 	= AdmissionPastHistory.objects.filter(admission_detail = adm_obj)
			adm_inv_obj						= AdmissionInv.objects.filter(admission_detail = adm_obj).order_by('created_at')
			adm_imaging_obj				= AdmissionImaging.objects.filter(admission_detail = adm_obj).order_by('created_at')
			adm_phy_exam_obj			= PhyExam.objects.filter(admission_detail = adm_obj).order_by('phy_exam_time')
			adm_procedure_obj			= ProcedureDetail.objects.filter(admission_detail = adm_obj)
			adm_discharge_obj			= DischargeDetail.objects.filter(admission_detail = adm_obj)

			data = {
			   "identifier": "id"   ,
			   "label"     : "name" ,
			   "items"     : [
							            {"name"  : "Complaints"   , "type":"sub", "id":"CMP",
							             'len'   : len(adm_complaint_obj),
							             "addUrl": adm_obj.get_admission_complaint_add_url()
							            },
							            {"name": "HPI"          , "type":"sub", "id":"HPI",
							             "len":len(adm_hpi_obj),
							             "addUrl": getattr(adm_obj, "get_admission_hpi_add_url",False)()
							            },
				                  {"name": "Past History" , "type":"sub", "id":"PH" ,
				                   "len":len(adm_past_history_obj),
							             "addUrl": getattr( adm_obj,"get_admission_past_history_add_url", False)()
				                  },
				                  {"name": "Investigation", "type":"sub", "id":"INV",
				                   "len" : len(adm_inv_obj),
							             "addUrl": adm_obj.get_admission_inv_add_url()
				                  },
				                  {"name": "Imaging"      , "type":"sub", "id":"IMAG" ,
				                   "len" : len(adm_imaging_obj),
							             "addUrl": adm_obj.get_admission_imaging_add_url()
				                  },
				                  {"name": "Physical Exam", "type":"sub", "id":"PHYEXAM" ,
				                   "len" : len(adm_phy_exam_obj),
							             "addUrl": adm_obj.get_admission_phy_exam_start_url()
				                  },
	#                       {"name": "Diagnosis"    , "type":"sub", "id":"DIAG" },
				                  {"name": "Procedures"   , "type":"sub", "id":"PROC" ,
				                   "len" : len(adm_procedure_obj),
							             "addUrl": adm_obj.get_admission_procedure_add_url()
				                  },
				                  {"name": "Discharge"    , "type":"sub", "id":"DIS" ,
				                   "len" : len(adm_discharge_obj),
							             "addUrl": getattr(adm_obj, "get_admission_discharge_add_url", False)()
				                  }
			              ]
			}

			if adm_complaint_obj:
				data['items'][0]['children'] = []
				children_list  = data['items'][0]['children']
				for complaint in adm_complaint_obj:
					dict_to_append = {"name":"", "type":"complaint", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = complaint.complaints + "- " + complaint.duration
					dict_to_append['id']      = "CMP_"+ unicode(complaint.id)
					dict_to_append['editUrl'] = complaint.get_admission_complaint_edit_url()
					dict_to_append['delUrl']  = complaint.get_admission_complaint_del_url()
					children_list.append(dict_to_append)

			if adm_hpi_obj:
				data['items'][1]['children'] = []
				children_list  = data['items'][1]['children']
				for hpi in adm_hpi_obj:
					dict_to_append = {"name":"", "type":"hpi", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = hpi.hpi[0:10]+"......"
					dict_to_append['id']      = "HPI_"+ unicode(hpi.id)
					dict_to_append['editUrl'] = hpi.get_admission_hpi_edit_url()
					dict_to_append['delUrl']  = hpi.get_admission_hpi_del_url()
					children_list.append(dict_to_append)

			if adm_past_history_obj:
				data['items'][2]['children'] = []
				children_list  = data['items'][2]['children']
				for ph in adm_past_history_obj:
					dict_to_append = {"name":"", "type":"past_history", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = ph.past_history[0:10]+"....."
					dict_to_append['id']      = "PH_"+ unicode(ph.id)
					dict_to_append['editUrl'] = ph.get_admission_past_history_edit_url()
					dict_to_append['delUrl']  = ph.get_admission_past_history_del_url()
					children_list.append(dict_to_append)

			if adm_inv_obj:
				data['items'][3]['children'] = []
				children_list  = data['items'][3]['children']
				for inv in adm_inv_obj:
					dict_to_append = {"name":"", "type":"investigation", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = inv.__unicode__()
					dict_to_append['id']      = "INV_"+ unicode(inv.id)
					dict_to_append['editUrl'] = inv.get_admission_inv_edit_url()
					dict_to_append['delUrl']  = inv.get_admission_inv_del_url()
					children_list.append(dict_to_append)

			if adm_imaging_obj:
				data['items'][4]['children'] = []
				children_list  = data['items'][4]['children']
				for imaging in adm_imaging_obj:
					dict_to_append = {"name":"", "type":"imaging", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = imaging.__trimmed_unicode__()
					dict_to_append['id']      = "IMAG_"+ unicode(imaging.id)
					dict_to_append['editUrl'] = imaging.get_admission_imaging_edit_url()
					dict_to_append['delUrl']  = imaging.get_admission_imaging_del_url()
					children_list.append(dict_to_append)

			if adm_phy_exam_obj:
				data['items'][5]['children'] = []
				children_list  = data['items'][5]['children']
				for pe in adm_phy_exam_obj:
					dict_to_append = {"name":"", "type":"phy_exam", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = pe.__trimmed_unicode__()
					dict_to_append['id']      = "PHYEXAM_"+ unicode(pe.id)
					dict_to_append['editUrl'] = pe.get_phy_exam_edit_url()
					dict_to_append['delUrl']  = pe.get_phy_exam_del_url()
					children_list.append(dict_to_append)

#			if adm_diagnosis_obj:
##				data['items'][6]['children'] = []
#				children_list  = data['items'][6]['children']
#				for d in adm_diagnosis_obj:
#					dict_to_append = {"name":"", "type":"diagnosis", "id":"","editUrl":"","delUrl":""}
#					dict_to_append['name']    = d.__unicode__()
#					dict_to_append['id']      = "DIAG_"+ unicode(d.id)
#					dict_to_append['editUrl'] = d.get_admission_diagnosis_edit_url()
#					dict_to_append['delUrl']  = d.get_admission_diagnogis_del_url()
#					children_list.append(dict_to_append)

			if adm_procedure_obj:
				data['items'][7]['children'] = []
				children_list  = data['items'][7]['children']
				for p in adm_procedure_obj:
					dict_to_append = {"name":"", "type":"procedure", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = p.__unicode__()
					dict_to_append['id']      = "PROC_"+ unicode(p.id)
					dict_to_append['editUrl'] = p.get_admission_procedure_edit_url()
					dict_to_append['delUrl']  = p.get_admission_procedure_del_url()
					children_list.append(dict_to_append)

			if adm_discharge_obj:
				data['items'][8]['children'] = []
				children_list  = data['items'][8]['children']
				for d in adm_discharge_obj:
					dict_to_append = {"name":"", "type":"discharge", "id":"","editUrl":"","delUrl":""}
					dict_to_append['name']    = d.__unicode__()
					dict_to_append['id']      = "DIS_"+ unicode(d.id)
					dict_to_append['editUrl'] = ph.get_admission_discharge_edit_url()
					dict_to_append['delUrl']  = ph.get_admission_discharge_del_url()
					children_list.append(dict_to_append)


			json = simplejson.dumps(data)
			return HttpResponse(json, content_type = "application/json")

		else:
			raise Http404("Invaild Request Method.")
	else:
		return HttpResponseRedirect('/login/')

################################################################################
@login_required
def render_admission_list(request):
    '''
    View for Generating Admission List
    Takes on Request Object as argument.
    '''
    user = request.user
    keys = ["sort( date_of_admission)", "sort(-date_of_admission)","sort(+date_of_admission)",
            "sort( surgeon)", "sort(-surgeon)", "sort(+surgeon)",
            ]
    key_sort_map = {
    "sort(+date_of_admission)": "date_of_admission",
    "sort( date_of_admission)": "date_of_admission",
    "sort(-date_of_admission)": "-date_of_admission",
    "sort(+surgeon)"       : "admitting_surgeon",
    "sort( surgeon)"       : "admittin_surgeon",
    "sort(-surgeon)"       : "-admitting_surgeon",
    }
    for key in request.GET:
      if key in keys:
        sort = key_sort_map[key]
        all_admissions = Admission.objects.all().order_by(sort)
      else:
        all_admissions = Admission.objects.all().order_by('date_of_admission')
    data         = []
    for admission in all_admissions:
      data_to_append = {}
      data_to_append['id']         = admission.id
      data_to_append['date_of_admission']   = admission.date_of_admission.strftime("%d/%m/%Y %H:%M:%S")
      data_to_append['surgeon']   = admission.admitting_surgeon.__unicode__()
      data_to_append['patient_hospital_id']   = admission.patient_detail.patient_hospital_id
      data_to_append['patient']    = admission.patient_detail.__unicode__()
      data_to_append['age']        = admission.patient_detail.age
      data_to_append['sex']        = admission.patient_detail.sex
      data_to_append['active']     = admission.admission_closed
      data_to_append['home']       = admission.get_admission_main_window_url()
      data.append(data_to_append)
    json = simplejson.dumps(data)
    print json
    return HttpResponse(json, content_type = "application/json")

################################################################################

#@login_required
#def admission_detail_list(request, id):
#  if request.method == 'GET':
#    user = request.user
#    try:
#      id 		       = int(id)
#      adm_obj      = Admission.objects.get(pk = id)
#      adm_obj_form = AdmissionForm(instance = adm_obj)
#    except (TypeError, ValueError, NameError, AttributeError):
#      raise Http404("Bad Request. Server Error")
#    except Admission.DoesNotExist:
#      raise Http404("Bad Request. Admission Detail Does not Exist.")
#    variable = RequestContext(request, {'user'         : user        ,
#                                        'adm_obj'      : adm_obj     ,
#                                        'adm_obj_form' : adm_obj_form
#                                       }
#                              )
#    return render_to_response( 'admission/detail/list.html',variable)
#  else:
#    raise Http404('Invalid request method')


@login_required
def admission_detail_edit(request, id):
  if request.method == 'GET' and request.is_ajax():
    user = request.user
    try:
      if not id:
        admission_id  = int(request.GET.get('admission_id'))
      else:
        admission_id = int(id)
      adm_obj           = Admission.objects.get(pk = admission_id)
    except (TypeError, ValueError, NameError, AttributeError):
      raise Http404("Bad Request. Server Error")
    except Admission.DoesNotExist:
      raise Http404("Bad Request. Admission Detail Does not Exist.")
    time              = 'T'+ adm_obj.time_of_admission.isoformat()
    date              = adm_obj.date_of_admission.isoformat()
    data              = {"time_of_admission": time, 'date_of_admission': date}
    print data
    adm_obj_edit_form = AdmissionForm(initial = data, instance = adm_obj)
    print adm_obj_edit_form
    variable = RequestContext(request, {'user'              : user        ,
                                        'adm_obj'           : adm_obj     ,
                                        'adm_obj_edit_form' : adm_obj_edit_form
                                       }
                              )
    return render_to_response( 'admission/detail/edit.html',variable)
  elif request.method == 'POST' and request.is_ajax():
    user = request.user
    try:
      id 		            = int(id)
      adm_obj           = Admission.objects.get(pk = id)
      request_post_copy = request.POST.copy()
      time              = request_post_copy['time_of_admission'][1:]
      request_post_copy['time_of_admission'] = time
      adm_obj_edit_form = AdmissionEditForm(request_post_copy, instance = adm_obj)
    except (TypeError, ValueError, NameError, AttributeError):
      raise Http404("Bad Request. Server Error")
    except Admission.DoesNotExist:
      raise Http404("Bad Request. Admission Detail Does not Exist.")
    if adm_obj_edit_form.is_valid():
     admission        = adm_obj_edit_form.save()
  
@login_required
def admission_detail_del(request, id):
  if request.method == 'GET' and request.is_ajax():
    user = request.user
    try:
      id 		            = int(id)
      adm_obj           = Admission.objects.get(pk = id)
    except (TypeError, ValueError, NameError, AttributeError):
      raise Http404("Bad Request. Server Error")
    except Admission.DoesNotExist:
      raise Http404("Bad Request. Admission Detail Does not Exist.")
    if user.is_superuser:
      adm_obj.delete()
#      return admission_list(request)
      if request.GET.get('redirect') and request.GET.get('redirect')==True:
        return HttpResponseRedirect('/admission/list/')
      else:
        success = True
        error_message = "Admission Deleted Successfully"
        form_errors = None
        data = { "success":success, 
                 "error_message": error_message, 
                 'form_errors': form_errors
               }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404('Bad request. Permission Denied.')
  else:
    raise Http404('Bad request. Invalid request.')


################################################################################
################################################################################

@login_required
def admission_past_history_main_window(request):
	if request.method == 'GET' and request.is_ajax():
		user 							= request.user
		admission_id 			= int(request.GET.get('admission_id'))
		adm_obj 					= Admission.objects.get(pk = admission_id)
		adm_past_history 	= AdmissionPastHistory.objects.filter(admission_detail = adm_obj)
		variable 					= RequestContext(request, { 'user'							:	user,
																									'adm_obj'						: adm_obj,
																									'adm_past_history'	:	adm_past_history
																									}
																			)
		return render_to_response( 'admission/past_history/main_window.html', variable )
	else:
		return Http404('This is non AJAX. This will not succeed')

@login_required
def admission_past_history_list(request):
	if request.method == 'GET' and request.is_ajax():
		user 							= request.user
		try:
			admission_id 			= int( request.GET.get('admission_id') )
			adm_obj 					= Admission.objects.get(pk = admission_id)
		except (KeyError, ValueError, AttributeError, NameError, TypeError):
			raise Http404("Incorrect Data Supplied. Please Try Again.")
		except Admission.DoesNotExist:
			raise Http404("Admission Data Does not exist.Please Try Again.")
		adm_past_history 	= AdmissionPastHistory.objects.filter(admission_detail = adm_obj)
		if adm_past_history:
			adm_past_history 			= adm_past_history[0]
			adm_past_history_form = AdmissionPastHistoryForm(instance = adm_past_history)
		else:
			adm_past_history 			= None
			adm_past_history_form = None
		variable 					= RequestContext(request, { 'user'									:	user, 
																									'adm_obj'								: adm_obj, 
																									'adm_past_history'			:	adm_past_history,
																									'adm_past_history_form'	: adm_past_history_form
																									}
																			)
		return render_to_response( 'admission/past_history/list.html', variable )
	else:
		return Http404('This is non AJAX. This will not succeed')

@login_required
def admission_past_history_add(request, id=None):
  user = request.user
  try:
    if id: 
      admission_id = int(id)
    else:
      if request.method == 'GET':
        admission_id 	= int(request.GET.get('admission_id'))
      elif request.method == 'POST':
        admission_id 	= int(request.POST.get('admission_id'))
      else:
        raise Http404("ERROR! Invaild Request Method..")
    adm_obj 				= Admission.objects.get(pk = admission_id)
    if adm_obj.has_past_history():
      raise Http404("ERROR! This Admission cannot add more Past History ")
    adm_past_history = AdmissionPastHistory(admission_detail = adm_obj)
  except(TypeError,AttributeError,ValueError,NameError,KeyError):
    raise Http404("ERROR ! : Invalid Arguments Requested.")
  except Admission.DoesNotExist:
    raise Http404("ERROR ! : Admission Does Not Exist")
  if request.method == 'GET' and request.is_ajax():
    adm_past_history_form = AdmissionPastHistoryForm(instance = adm_past_history)
    variable = RequestContext(request, {'user'									: user,
                                        'adm_obj'								: adm_obj,
                                        'adm_past_history'			: adm_past_history,
                                        'adm_past_history_form' : adm_past_history_form,
                                        })
    return render_to_response('admission/past_history/add.html', variable)
  elif request.method == 'POST' and request.is_ajax():
    adm_past_history_form = AdmissionPastHistoryForm(request.POST, instance = adm_past_history)
    if adm_past_history_form.is_valid():
      adm_past_history_saved = adm_past_history_form.save()
      success = True
      error_message = 'Saved Successfully'
      form_errors = adm_past_history_form.errors
      data = {	'success'						:	success				, 
								'error_message'			:	error_message	, 
								'form_errors'				:	form_errors		, 
							}
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      success       = False
      form_errors   = adm_past_history_form.errors
      error_message = "ERROR ! Past History Could not be added..."
      data = {'success':success, 'error_message':error_message, 'form_errors':form_errors}
      variable = RequestContext(request, {'user'									:	user									,
						                              'adm_obj'								:	adm_obj								,
						                              'adm_past_history'			:	adm_past_history			,
						                              'adm_past_history_form'	:	adm_past_history_form	,
						                              }
						                   )
      return render_to_response('admission/past_history/add.html', variable)
  else:
    raise Http404("Bad Request. If this is non AJAX it will not work", request.method )


@login_required
def admission_past_history_edit(request, id=None):
	user = request.user
	try:
		if id: 
			past_history_id = int(id)
		else:
			if request.method == 'GET':
				past_history_id 	= int(request.GET.get('past_history_id'))
			elif request.method == 'POST':
				past_history_id 	= int(request.POST.get('past_history_id'))
			else:
				raise Http404("ERROR! Invaild Request Method..")
		past_history_obj = AdmissionPastHistory.objects.get(pk = past_history_id)
	except(NameError,ValueError,AttributeError,KeyError):
		raise Http404("ERROR! : Invalid Request Parameters")
	except(AdmissionPastHistory.DoesNotExist):
		raise Http404("ERROR! : Requested Admission Past History Does Not Exist.")
	if request.is_ajax() and request.method == 'GET':
		past_history_form = AdmissionPastHistoryForm(instance = past_history_obj)
		variable          = RequestContext(request, {'user'			:	user	            ,
																				'past_history_id'		:	past_history_id		,
																				'past_history_obj'	:	past_history_obj	,
																				'past_history_form'	:	past_history_form	,
																				}
															)
		return render_to_response('admission/past_history/edit.html', variable)
	if request.is_ajax() and request.method == 'POST':
		past_history_form = AdmissionPastHistoryForm(request.POST, instance = past_history_obj)
		if past_history_form.is_valid():
			saved_past_history = past_history_form.save()
			success            = True
			error_message      = "Successfully Edited"
			form_errors        = past_history_form.errors
		else:
			success 	     = False
			error_message  = "Error Occured. Past History Could not be edited "
			form_errors    = past_history_form.errors
		data = {	'success'				:	success				, 
								'error_message'	:	error_message	, 
								'form_errors'		:	form_errors		, 
							}
		json = simplejson.dumps(data)
		return HttpResponse(json, content_type = 'application/json')
	else:
		raise Http404('This is non - AJAX request. This will not work')

@login_required
def admission_past_history_del(request, id=None):
	if request.is_ajax() and request.method == 'GET':
		user = request.user
		try:
			if id:
				past_history_id = int(id)
			elif(request.GET.get('past_history_id')):
				past_history_id = int( request.GET.get('past_history_id') )
			else:
				raise Http404("ERROR! : Invalid Request Parameters")
			past_history_obj = AdmissionPastHistory.objects.get(pk = past_history_id)
		except(ValueError, AttributeError, TypeError, AdmissionPastHistory.DoesNotExist):
			raise Http404('The requested data does not exist')
		except(AdmissionPastHistory.DoesNotExist, KeyError):
			raise Http404('ERROR! The requested Past History does not exist')
		if user.is_superuser and user.is_authenticated:
			past_history_obj.delete()
			success = True
			error_message = "Successfully Deleted"
		else:
			success = False
			error_message = "Insufficient Priviliges"
		data = {'success':success, 'error_message':error_message}
		json = simplejson.dumps(data)
		return HttpResponse(json, content_type = 'application/json')
	else:
		raise Http404('Bad Request. This is Non AJAX and will not work.')

################################################################################

####################################################################################################

@login_required
def admission_hpi_list(request):
	if request.method == 'GET' and request.is_ajax():
		user 					= request.user
		admission_id 	= int(request.GET.get('admission_id'))
		adm_obj 			= Admission.objects.get(pk = admission_id)
		adm_hpi 			= AdmissionHPI.objects.filter(admission_detail = adm_obj)
		if not adm_hpi:
			adm_hpi 					= None
			adm_hpi_form 			= None
			adm_hpi_add 			= AdmissionHPI(admission_detail = adm_obj)
			adm_hpi_add_form 	= AdmissionHPIForm(instance = adm_hpi_add)
		else:
			adm_hpi 					= adm_hpi[0]
			adm_hpi_form 			= AdmissionHPIForm( instance = adm_hpi )
			adm_hpi_add				= None
			adm_hpi_add_form 	= None
		if adm_hpi:
			print "Admission HPI is there"
		else:
			print "No HPIs..."
		print "Admission HPI: ", adm_hpi
		variable = RequestContext(request, {'user'						: user,
																				'adm_obj'					: adm_obj,
																				'adm_hpi'					: adm_hpi,
																				'adm_hpi_form'		: adm_hpi_form,
																				'adm_hpi_add'			: adm_hpi_add,
																				'adm_hpi_add_form': adm_hpi_add_form
																			})
		return render_to_response( 'admission/hpi/list.html', variable )
	else:
		return Http404('This is non AJAX. This will not succeed')

@login_required
def admission_hpi_add(request, id=None):
  user = request.user
  try:
    if id: 
      admission_id = int(id)
    else:
      if request.method == 'GET':
        admission_id 	= int(request.GET.get('admission_id'))
      elif request.method == 'POST':
        admission_id 	= int(request.POST.get('admission_id'))
      else:
        raise Http404("ERROR! Invaild Request Method..")
    adm_obj 				= Admission.objects.get(pk = admission_id)
    if adm_obj.has_hpi():
      raise Http404("ERROR! This Admission cannot add more ")
  except(TypeError,AttributeError,ValueError,NameError,KeyError):
    raise Http404("ERROR ! : Invalid Arguments Requested.")
  except Admission.DoesNotExist:
    raise Http404("ERROR ! : Admission Does Not Exist")
  adm_hpi 			= AdmissionHPI(admission_detail = adm_obj)
  if request.method == 'GET' and request.is_ajax():
    print "Received GET request to add HPI"
    adm_hpi_form 	= AdmissionHPIForm(instance = adm_hpi)
    variable 			= RequestContext(request, {	'user'					: user,
																							'adm_obj'				: adm_obj,
																							'adm_hpi'				: adm_hpi,
																							'adm_hpi_form' 	: adm_hpi_form,
																						})
    return render_to_response('admission/hpi/add.html', variable)
  elif request.method == 'POST' and request.is_ajax():
    print "Received POST request to add HPI"
    print request.POST
    adm_hpi_form 		= AdmissionHPIForm(request.POST, instance = adm_hpi)
    if adm_hpi_form.is_valid():
      adm_hpi_saved = adm_hpi_form.save()
      success 			= True
      error_message = 'Saved Successfully'
      form_errors 	= adm_hpi_form.errors
      print "INFO: HPI Form Validated successfully and HPI added.."
      data 					= {	'success'				:	success				,
												'error_message'	:	error_message	,
												'form_errors'		:	form_errors		,
											}
      json 					= simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      print "ERROR ! HPI Form didt not Validate successfully"
      success 			= False
      form_errors 	= adm_hpi_form.errors
      desc_form_errors = ''
#      for key,value in form_errors:
#        desc_form_errors += key+" :\t" +value + "\n"
      print "ERRORS FOUND: "
      print form_errors
      error_message = "Please correct the errors: "+ str(adm_hpi_form.errors)
      data 					= {	'success'				:	success					,
												'error_message'	:	error_message		,
												'form_errors'		:	form_errors
											}
      variable 			= RequestContext(request, {	'user'				:	user,
																								'adm_obj'			:	adm_obj,
																								'adm_hpi'			:	adm_hpi,
																								'adm_hpi_form':	adm_hpi_form,
																							})
      return render_to_response('admission/hpi/add.html', variable)
  else:
    raise Http404("Bad Request. If this is non AJAX it will not work")


@login_required
def admission_hpi_edit(request, id= None):
  user = request.user
  try:
    if id: 
      hpi_id = int(id)
    else:
      if request.method == 'GET':
        hpi_id 	= int(request.GET.get('hpi_id'))
      elif request.method == 'POST':
        hpi_id 	= int(request.POST.get('hpi_id'))
      else:
        raise Http404("ERROR! Invaild Request Method..")
    hpi_obj 				= AdmissionHPI.objects.get(pk = hpi_id)
  except(TypeError,AttributeError,ValueError,NameError,KeyError):
    raise Http404("ERROR ! : Invalid Arguments Requested.")
  except (AdmissionHPI.DoesNotExist):
    raise Http404("ERROR ! : Admission HPI Does Not Exist")
  if request.is_ajax() and request.method == 'GET':
    hpi_form = AdmissionHPIForm(instance = hpi_obj)
    variable = RequestContext(request, {'user'					:user,
																				'hpi_id'	:hpi_id,
																				'hpi_obj'	:hpi_obj,
																				'hpi_form':hpi_form,
																				})
    return render_to_response('admission/hpi/edit.html', variable)
  if request.is_ajax() and request.method == 'POST':
    hpi_form = AdmissionHPIForm(request.POST, instance = hpi_obj)
    if hpi_form.is_valid():
      saved_hpi     = hpi_form.save()
      hpi           = saved_hpi.hpi
      success       = True
      error_message = "Successfully Edited"
      form_errors   = hpi_form.errors
      data          = {'success'       : success, 
                       'error_message' : error_message, 
                       'form_errors'   : form_errors, 
                       'hpi'           : hpi
                      }
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      success       = False
      error_message = "Error Occured " + hpi_form.errors
      form_errors   = hpi_form.errors
      data          = { 'success'       : success, 
                        'error_message' : error_message, 
                        'form_errors'   : form_errors
                      }
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404('This is non - AJAX request. This will not work')



@login_required
def admission_hpi_del(request, id = None):
	user = request.user
	if request.is_ajax() and request.method == 'GET':
		success 			= False
		error_message = "Deleted Successfully"
		try:
			if id:
				hpi_id = int(id)
			else:
				hpi_id = int(request.GET.get('hpi_id'))
			hpi_obj = AdmissionHPI.objects.get(pk = hpi_id)
		except(ValueError, AttributeError, KeyError, NameError,TypeError):
			raise Http404("ERROR ! Invalid Request Parameters.")
		except(AdmissionHPI.DoesNotExist):
			raise Http404("ERROR !! : The Requested Data Does not Exist. Please try again.")
		if user.is_superuser and user.is_authenticated:
			hpi_obj.delete()
			success 			= True
		else:
			error_message = "Insufficient Priviliges. Cannot Delete"
		data = {'success':success, 'error_message':error_message}
		json = simplejson.dumps(data)
		return HttpResponse(json, content_type = 'application/json')
	else:
		raise Http404('Bad Request. This is Non AJAX and will not work.')


################################################################################


@login_required
def admission_complaints_main_window(request):
	if request.method == 'GET' and request.is_ajax():
		user = request.user
		try:
			admission_id = int( request.GET.get('admission_id') )
			adm_obj = Admission.objects.get( pk = admission_id )
		except(ValueError, AttributeError, NameError, TypeError):
			raise Http404("Bad Request:: Invalid Data Supplied.")
		except(Admission.DoesNotExist):
			raise Http404("Bad Request:: Invalid Data Supplied. No Such Admission Data !! ")
		variable = RequestContext( request, {	'user'					: user					,
																					'adm_obj'				: adm_obj				,
																				}
															)
		print "Loading Complaints Main Window"
		return render_to_response( 'admission/complaints/main_window.html', variable )
	else:
		return Http404( 'This is non AJAX. This will not succeed' )

@login_required
def admission_complaints_list(request, id=None):
	print "Received Request to list all complaints for this admission ..."
	if request.method == 'GET' and request.is_ajax():
		user = request.user
		try:
			if id:
				admission_id = int(id)
			else:
				admission_id 		= int(request.GET.get('admission_id'))
			adm_obj 				= Admission.objects.get(pk = admission_id)
			adm_complaints 	= AdmissionComplaint.objects.filter(admission_detail = adm_obj)
			adm_complaints_form_list = []
		except(ValueError, AttributeError, NameError, TypeError):
			raise Http404("Bad Request:: Invalid Data Supplied.")
		except(Admission.DoesNotExist):
			raise Http404("Bad Request:: Invalid Data Supplied. No Such Admission Data !! ")
		if len(adm_complaints) >0:
			for complaint in adm_complaints:
				adm_complaint_form = AdmissionComplaintForm(instance = complaint)
				list_to_append  = [adm_complaint_form, complaint]
				adm_complaints_form_list.append(list_to_append)
		variable = RequestContext(request, { 'user'						         : user	 			,
																				 'adm_obj'				         : adm_obj			,
																				 'adm_complaints'	         : adm_complaints,
																				 'adm_complaints_form_list': adm_complaints_form_list
																				}
															)
		print "Listing all Complaints "
		return render_to_response( 'admission/complaints/list.html', variable )
	else:
		return Http404('This is non AJAX. This will not succeed')

@login_required
def admission_complaints_add(request, id=None):
	if request.method == 'GET' and request.is_ajax():
		user = request.user
		try:
			if id:
				admission_id = int(id)
			else:
				admission_id 	= int( request.GET.get('admission_id') )
			adm_obj 			= Admission.objects.get( pk = admission_id )
		except(ValueError, AttributeError, NameError, TypeError):
			raise Http404("Bad Request:: Invalid Data Supplied.")
		except(Admission.DoesNotExist):
			raise Http404("Bad Request:: Invalid Data Supplied. No Such Admission Data !! ")
		adm_complaint 			= AdmissionComplaint(admission_detail = adm_obj)
		adm_complaint_form 	= AdmissionComplaintForm(instance = adm_complaint)
		variable 						= RequestContext(request, {	'user'								: user								,
																										'adm_obj'							: adm_obj							,
																										'adm_complaint'				: adm_complaint				,
																										'adm_complaint_form' 	: adm_complaint_form	,
																										}
																				)
		return render_to_response('admission/complaints/add.html', variable)
	elif request.method == 'POST' and request.is_ajax():
		user = request.user
		try:
			if id:
				admission_id = int(id)
			else:
				admission_id 	= int( request.POST.get('admission_detail') )
			adm_obj 			= Admission.objects.get( pk = admission_id )
		except(ValueError, AttributeError, NameError, TypeError):
			raise Http404("Bad Request:: Invalid Data Supplied.")
		except(Admission.DoesNotExist):
			raise Http404("Bad Request:: Invalid Data Supplied. No Such Admission Data !! ")
		adm_complaint 			= AdmissionComplaint(admission_detail = adm_obj)
		adm_complaint_form 	= AdmissionComplaintForm(request.POST, instance = adm_complaint)
		if adm_complaint_form.is_valid():
			adm_complaint_saved = adm_complaint_form.save()
			all_complaints 			= AdmissionComplaint.objects.filter(admission_detail = adm_obj)
			complaint_list 			= []
			for complaint in all_complaints:
				complaint_list.append(complaint.complaints)
			success 			= True
			error_message = 'Saved Successfully'
			form_errors 	= adm_complaint_form.errors
			data 					= {	'success'				: success				,
												'error_message'	: error_message	,
												'form_errors'		: form_errors		,
												'complaint_list': complaint_list
											}
			json 					= simplejson.dumps(data)
			return HttpResponse(json, content_type = 'application/json')
		else:
			success 			= False
			form_errors 	= adm_complaint_form.errors
			error_list		= ""
			for error in form_errors:
				error_list 	+= '<p class="error_message">' + error + '</p>'
			error_message 	= " Sorry!! There were Errors. Form was not saved. Please correct the errors "
			data 						= {	'success'				: success				,
														'error_message'	: error_message	,
														'form_errors'		: form_errors		,
														'error_list'		: error_list
													}
			json 						= simplejson.dumps(data)
			return HttpResponse(json, content_type = 'application/json')
	else:
		raise Http404("Bad Request. If this is non AJAX it will not work")


@login_required
def admission_complaints_edit(request, id=None):
	user = request.user
	if request.is_ajax() and request.method == 'GET':
		try:
			if id:
				complaint_id = int(id)
			else:
				complaint_id 		= int(request.GET.get('complaint_id'))
			complaint_obj 	= AdmissionComplaint.objects.get(pk = complaint_id)
			complaint_form 	= AdmissionComplaintForm(instance = complaint_obj)
		except(ValueError, AttributeError, NameError, TypeError, KeyError):
			raise Http404("Bad Request:: Invalid Data Supplied.")
		except(AdmissionComplaint.DoesNotExist):
			raise Http404("Bad Request:: Invalid Data Supplied. No Such Admission Data !! ")
		action 					= '/admission/complaints/edit/'
		method 					= 'post'
		button 					= 'Edit'
		print complaint_form
		variable 				= RequestContext(request, {	'user'					:user,
																								'complaint_id'	:complaint_id,
																								'complaint_obj'	:complaint_obj,
																								'complaint_form':complaint_form,
																								'action'				:action,
																								'method'				:method,
																								'button'				:button
																							}
																		)
		return render_to_response('admission/complaints/edit.html', variable)
	if request.is_ajax() and request.method == 'POST':
		try:
			if id:
				complaint_id = int(id)
			else:
				complaint_id 		= int(request.POST.get('complaint_id'))
			complaint_obj 	= AdmissionComplaint.objects.get(pk = complaint_id)
			complaint_form 	= AdmissionComplaintForm(request.POST, instance = complaint_obj)
		except(ValueError, AttributeError, NameError, TypeError, KeyError):
			raise Http404("Bad Request:: Invalid Data Supplied.")
		except(AdmissionComplaint.DoesNotExist):
			raise Http404("Bad Request:: Invalid Data Supplied. No Such Admission Data !! ")
		if complaint_form.is_valid():
			saved_complaint = complaint_form.save()
			complaint 			= saved_complaint.complaints
			duration 				= saved_complaint.duration
			success 				= True
			error_message 	= "Successfully Edited"
			form_errors 		= complaint_form.errors
			data 						= {	'success'				:	success				,
													'error_message'	:	error_message	,
													'form_errors'		:	form_errors		,
													'complaint'			:	complaint			,
													'duration'			:duration
												}
			json 						= simplejson.dumps(data)
			return HttpResponse(json, content_type = 'application/json')
		else:
			success 			= False
			error_message 	= " Sorry!! There were Errors. Form was not saved. Please correct the errors "
			form_errors 	= complaint_form.errors
			error_list		= ""
			for error in form_errors:
				error_list 	+= '<p class="error_message">' + error + '</p>'
			data = {	'success'				:	success				,
								'error_message'	:	error_message	,
								'form_errors'		:	form_errors		,
								'error_list'		: error_list
							}
			json = simplejson.dumps(	data	)
			return HttpResponse(json, content_type = 'application/json')
	else:
		raise Http404('This is non - AJAX request. This will not work')

@login_required
def admission_complaints_del(request, id=None):
	if request.user:
		user = request.user
		if request.is_ajax() and request.method == 'GET':
			try:
				if id:
					complaint_id = int(id)
				else:
					complaint_id 	= int(request.GET.get('complaint_id'))
				complaint_obj = AdmissionComplaint.objects.get(pk = complaint_id)
			except(ValueError, AttributeError, TypeError, AdmissionComplaint.DoesNotExist):
				raise Http404('The requested data does not exist')
			if user.is_superuser and user.is_authenticated:
				complaint_obj.delete()
				success 			= 	True
				error_message = 	"Successfully Deleted"
			else:
				success 			=	 	False
				error_message = 	"Insufficient Priviliges"
			data = {'success':success, 'error_message':error_message}
			json = simplejson.dumps(data)
			return HttpResponse(json, content_type = 'application/json')
		else:
			raise Http404('Bad Request. This is Non AJAX and will not work.')
	else:
		raise Http404('Insufficient Priviliges. You have to log in to delete')


####################################################################################################


@login_required
def incidentreport_ip_list(request, id):
	if request.method == 'GET' and request.is_ajax():
		user 								= request.user
		admission_id 				= int(id)
		adm_obj 						= Admission.objects.get(pk = admission_id)
		incidentreport_obj 	= IncidentReport.objects.filter(admission_detail = adm_obj)
		if incidentreport_obj:
			variable = RequestContext(request, {'user'							 	: user								,
																					'incidentreport_obj' 	: incidentreport_obj	,
																					'adm_obj'							: adm_obj							,
																					'admission_id'				: admission_id				,
																				})
			return render_to_response( 'admission/incidentreport/list.html', variable )
		else:
			return incidentreport_ip_add(request, id)
	else:
		return Http404('This is non AJAX. This will not succeed')

@login_required
def incidentreport_ip_add(request, id):
  if request.method == 'GET' and request.is_ajax():
    user 									= request.user
    admission_id 					= int(id)
    adm_obj 							= Admission.objects.get(pk = admission_id)
    incidentreport_obj 		= IncidentReport(admission_detail = adm_obj)
    incidentreport_form 	= AdmissionIncidentReportForm(instance = incidentreport_obj)
    variable = RequestContext(request, {'user'									: user									,
																				'adm_obj'								: adm_obj								,
																				'incidentreport_obj'		: incidentreport_obj		,
																				'incidentreport_form'		: incidentreport_form		,
																				})
    return render_to_response('admission/incidentreport/add.html', variable)
  elif request.method == 'POST' and request.is_ajax():
    user 									= request.user
    admission_id 					= int(id)
    adm_obj 							= Admission.objects.get(pk = admission_id)
    incidentreport_obj 		= IncidentReport(admission_detail = adm_obj)
    incidentreport_form 	= AdmissionIncidentReportForm(request.POST,instance = incidentreport_obj)
    if incidentreport_form.is_valid():
      incident_saved 	= incidentreport_form.save()
      all_incidents 	= IncidentReport.objects.filter(admission_detail = adm_obj)
      success 				= True
      error_message 	= 'Saved Successfully'
      form_errors 		= incidentreport_form.errors
      data 						= {	'success'						:	success				, 
													'error_message'			:	error_message	, 
													'form_errors'				:	form_errors		, 
												}
      json 						= simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      success 			= False
      form_errors 	= incidentreport_form.errors
      error_message = "Error ! Form could not be saved. Please correct the errors " 
      data = {	'success'				:	success				, 
      					'error_message'	:	error_message	, 
      					'form_errors'		:	form_errors
      				}
      json 	= simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404("Bad Request. If this is non AJAX it will not work", request.method )


@login_required
def incidentreport_ip_edit(request, id):
	print 'Received Request to Edit Incident....'
	user = request.user
	if request.method == 'GET' and request.is_ajax():
		try:
			incident_id = int(id)
			incidentreport_obj = IncidentReport.objects.get(pk = incident_id)
		except(KeyError, NameError, AttributeError, ValueError, TypeError):
			raise Http404('Bad Request. Invalid Data Supplied')
		except(IncidentReport.DoesNotExist):
			raise Http404('Bad Request. Requested Incident Data Does Not Exist.')
		incidentreport_form = AdmissionIncidentReportForm(instance = incidentreport_obj)
		variable 						= RequestContext(request, {	'user'								: user									, 
																										'incidentreport_obj'	: incidentreport_obj		,
																										'incidentreport_form'	: incidentreport_form		,
																										})
		return render_to_response('admission/incidentreport/edit.html', variable)
	if request.method == 'POST' and request.is_ajax():
		try:
			incident_id = int(id)
			incidentreport_obj = IncidentReport.objects.get(pk = incident_id)
		except(KeyError, NameError, AttributeError, ValueError, TypeError):
			raise Http404('Bad Request. Invalid Data Supplied')
		except(IncidentReport.DoesNotExist):
			raise Http404('Bad Request. Requested Incident Data Does Not Exist.')
		incidentreport_form = AdmissionIncidentReportForm(request.POST, instance = incidentreport_obj)
		if incidentreport_form.is_valid():
			saved_incident 	= incidentreport_form.save()
			success					= True
			error_message 	= "Incident Edited Successfully"
			form_errors 		= incidentreport_form.errors
		else:
			saved_incident 	= incidentreport_form.save()
			success					= False
			error_message 	= "Error! . Incident Could not be Edited"
			form_errors 		= incidentreport_form.errors
		data = {	'success'				: success				, 
							'error_message'	: error_message	, 
							'form_errors'		: form_errors
						}
		json 	= simplejson.dumps(data)
		return HttpResponse(json, content_type = 'application/json')
	else:
		raise Http404('Bad Request Method.')

@login_required
def incidentreport_ip_del(request, id):
	user = request.user
	if user.is_superuser:
		if request.method == 'GET' and request.is_ajax():
			try:
				incident_id = int(id)
				incidentreport_obj = IncidentReport.objects.get(pk = incident_id)
			except(KeyError, NameError, AttributeError, ValueError, TypeError):
				raise Http404('Bad Request. Invalid Data Supplied')
			except(IncidentReport.DoesNotExist):
				raise Http404('Bad Request. Requested Incident Data Does Not Exist.')
			incidentreport_obj.delete()
			success					= True
			error_message 	= "Incident Deleted Successfully"
			form_errors 		= None
			data = {	'success'				: success				, 
								'error_message'	: error_message	, 
								'form_errors'		: form_errors
							}
			json 	= simplejson.dumps(data)
			return HttpResponse(json, content_type = 'application/json')
		else:
			raise Http404('Bad Request: Improper request method./ Non-Ajax method')
	else:
		success					= False
		error_message 	= "Permission denied. Cannot Delete."
		form_errors 		= True
		data = {	'success'				: success				, 
							'error_message'	: error_message	, 
							'form_errors'		: form_errors
						}
		json 	= simplejson.dumps(data)
		return HttpResponse(json, content_type = 'application/json')


################################################################################

@login_required
def sf36_add(request, id):
	return render_to_response('scoring/SF-36.html')

