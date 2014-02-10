################################################################################
# Physical Examination Views for AuShadha
# Takes care of all the Physical Examination Related Data.
# Author    : Dr.Easwar T.R
# Copyright : 2012
# Date      : 2012-12-31
# License   : GNU-GPL Version 3
################################################################################


# General Module imports-----------------------------------
import StringIO
#import ho.pisa as pisa
from reportlab.pdfgen import canvas
from datetime import datetime, date, time
import yaml
import importlib

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
#from django.core.context_processors  import csrf
#from django.views.decorators.csrf    import csrf_exempt

# Application Specific Model Imports-----------------------

from AuShadha.settings import LOGIN_URL
from AuShadha.apps.ui.ui import ui as UI

from patient.models import *
from patient.views import *
from admission.models import *
from visit.models import *
from phyexam.models import *


################################################################################
#
# NEW VIEWS 
#
################################################################################
@login_required
def vascular_exam_add(request,id=None):
  pass

@login_required
def vascular_exam_list(request,id=None):
  pass

@login_required
def vascular_exam_edit(request,id=None):
  pass

@login_required
def vascular_exam_del(request,id=None):
  error_message = "Successfully Deleted Vascular Exam."
  success = True
  if request.method == "GET" and request.is_ajax():
      user = request.user
      if user.has_perm('phyexam.delete_vascexam_freemodel'):
          try:
              id = int(id)
              vasc_exam_obj = VascExam_FreeModel.objects.get(pk=id)
              vasc_exam_obj.delete()
          except (TypeError, NameError, ValueError, AttributeError, KeyError):
              error_message = "Error ! Invalid Request Parameters. "
              success = False
          except (VisitDetail.DoesNotExist):
              success = False            
              error_message = "Requested Vascular Exam Does not exist."
      else:
          success = False
          error_message = "Insufficient Permission. Could not delete."
      data = {'success': success, 'error_message': error_message}
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type='application/json')
  else:
      raise Http404(" Error ! Unsupported Request..")



















################################################################################
#
# OLD VIEWS - DO NOT USE / EXTEND
# Kept only for compatibility while migrating
#
################################################################################

#AUTHENTICATED_OBJ_LIST = ['vital', 'gen', 'sys', 'vasc', 'neuro']

#EXAM_OBJ_MAP = {'vital': VitalExam,
                #'sys': SysExam,
                #'gen': GenExam,
                #'vasc': VascExam,
                #'neuro': PeriNeuroExam
                #}

#EXAM_FORM_MAP = {'vital': OP_VitalExamForm,
                 #'sys': OP_SysExamForm,
                 #'gen': OP_GenExamForm,
                 #'vasc': OP_VascExamForm,
                 #'neuro': OP_PeriNeuroExamForm
                 #}


#def _return_obj_and_form(obj_to_add, phyexam_obj, request):
    #"""This returns the Object and the Form to add.

    #Takes three arguments,     the obj_to_add as String     the PhyExam
    #object instance     the request object

    #"""
    #if obj_to_add in AUTHENTICATED_OBJ_LIST:
        #model = EXAM_OBJ_MAP[obj_to_add]
        #form = EXAM_FORM_MAP[obj_to_add]
        #obj = model(phyexam=phyexam_obj)
        #if request.method == 'GET':
            #return_form = form(phyexam=phyexam_obj)
        #elif request.method == 'POST':
            #return_form = form(request.POST, instance=phyexam_obj)
        #else:
            #raise Exception("Unsupported Request Method")
        #return dict({'obj': obj, 'form': obj})
    #else:
        #raise Exception("This is not an accepted Examination Object.")


#@login_required
#def add_exams(request, exam_to_add, id=None):

    #if request.user:
        #user = request.user

        #if id:
            #try:
                #id = int(id)
                #phyexam_obj = PhyExam.objects.get(pk=id)
        #else:
            #try:
                #id = int(request.GET.get('phyexam_id'))
                #phyexam_obj = PhyExam.objects.get(pk=id)
            #except (PhyExam.DoesNotExist, ValueError, NameError, AttributeError, KeyError, TypeError):
                #raise Http404(" ERROR! Bad Request Attributes. Please retry.")
        #exam_obj = _return_obj_and_form(
            #exam_to_add, phyexam_obj, request)['return_form']
        #exam_form = _return_obj_and_form(
            #exam_to_add, phyexam_obj, request)['return_form']

        #if request.method == 'GET' and request.is_ajax():
            #variable = RequestContext(request, {'user': user,
                                                #'pat_obj': phyexam_obj.visit_detail.patient_detail,
                                                #'phyexam_obj': phyexam_obj,
                                                #'exam_obj': exam_obj,
                                                #'exam_form': exam_form
                                                #})
            #return render_to_response('phyexam/visit/add_%s.html' % (exam_to_add), variable)

        #if request.method == 'POST' and request.is_ajax():
            #if exam_form.is_valid():
                #saved_exam = exam_form.save()
                #success = True
                #error_message = "%s Examination Saved Successfully" % (
                    #exam_to_add.capitalize())
                #form_errors = None
            #else:
                #success = False
                #error_message = "ERROR! %s Examination form could not be saved" % (
                    #exam_to_add.capitalize())
                #form_errors = exam_form.errors
            #data = {'success': success, 'error_message': error_message, 'form_errors':
                    #form_errors}
            #json = simplejson.dumps(data)
            #return HttpResponse(json, content_type='application/json')
        #else:
            #raise Http404("Bad Request / Request method")
    #else:
        #return HttpResponseRedirect(settings.LOGIN_URL)


#@login_required
#def exams_edit(request, exam_to_edit, id=None):

    #if request.user:
        #user = request.user

        #if exam_to_edit in AUTHENTICATED_OBJ_LIST:
            #exam_to_edit = EXAM_OBJ_MAP[exam_to_edit]
            #exam_form = EXAM_FORM_MAP[exam_to_edit]
        #else:
            #raise Exception("Invalid Exam Requested")
            #print 'Invalid request for an exam... defaulting to Vitals'

        #if id:
            #try:
                #id = int(id)
                #exam_obj = exam_to_edit.objects.get(pk=id)
        #else:
            #try:
                #id = int(request.GET.get('exam_id'))
                #exam_obj = exam_to_edit.objects.get(pk=id)
            #except (exam_to_edit.DoesNotExist, ValueError, NameError, AttributeError, KeyError, TypeError):
                #raise Http404(" ERROR! Bad Request Attributes. Please retry.")

        #if request.method == 'GET' and request.is_ajax():
            #exam_form = exam_form(instance=exam_obj)
            #variable = RequestContext(request, {'user': user,
                                                #'pat_obj': phyexam_obj.visit_detail.patient_detail,
                                                #'phyexam_obj': exam_obj.phyexam,
                                                #'exam_obj': exam_obj,
                                                #'exam_form': exam_form
                                                #})
            #return render_to_response('phyexam/visit/edit_%s.html' % (exam_to_add), variable)

        #if request.method == 'POST' and request.is_ajax():
            #exam_form = exam_form(request.POST, instance=exam_obj)
            #if exam_form.is_valid():
                #saved_exam = exam_form.save()
                #success = True
                #error_message = "%s Examination Saved Successfully" % (
                    #exam_to_edit.capitalize())
                #form_errors = None
            #else:
                #success = False
                #error_message = "ERROR! %s Examination form could not be saved" % (
                    #exam_to_edit.capitalize())
                #form_errors = exam_form.errors
            #data = {'success': success, 'error_message': error_message, 'form_errors':
                    #form_errors}
            #json = simplejson.dumps(data)
            #return HttpResponse(json, content_type='application/json')
        #else:
            #raise Http404("Bad Request / Request method")
    #else:
        #return HttpResponseRedirect(settings.LOGIN_URL)


#@login_required
#def exams_del(request, exam, id=None):

    #if request.user:
        #user = request.user

        #if exam in AUTHENTICATED_OBJ_LIST:
            #exam_name = EXAM_OBJ_MAP[exam]
        #else:
            #raise Exception("Invalid Exam Requested")
            #print 'Invalid request for an exam... defaulting to Vitals'

        #if id:
            #try:
                #id = int(id)
                #exam_obj = exam_name.objects.get(pk=id)
        #else:
            #try:
                #id = int(request.GET.get('exam_id'))
                #exam_obj = exam_name.objects.get(pk=id)
            #except (exam_name.DoesNotExist, ValueError, NameError, AttributeError, KeyError, TypeError):
                #raise Http404(" ERROR! Bad Request Attributes. Please retry.")

            #if request.method == 'GET' and request.is_ajax():
                #exam_obj.delete()
                #success = True
                #error_message = "%s Examination Deleted Successfully" % (
                    #exam.capitalize())
                #form_errors = None
                #data = {'success': success, 'error_message': error_message, 'form_errors':
                        #form_errors}
                #json = simplejson.dumps(data)
                #return HttpResponse(json, content_type='application/json')
            #else:
                #raise Http404("Bad Request / Request method")

        #else:
            #success = False
            #error_message = "ERROR! Permission Denied"
            #form_errors = None
            #data = {'success': success, 'error_message': error_message, 'form_errors':
                    #form_errors}
            #json = simplejson.dumps(data)
            #return HttpResponse(json, content_type='application/json')

    #else:
        #return HttpResponseRedirect(settings.LOGIN_URL)


#@login_required
#def phyexam_add(request, id=None):
    #if request.user:
        #user = request.user
        #if id:
            #try:
                #id = int(id)
                #visit_obj = VisitDetail.objects.get(pk=id)
                #pat_obj = visit_obj.patient_detail
        #else:
            #try:
                #id = int(request.GET.get('visit_id'))
                #visit_obj = VisitDetail.objects.get(pk=id)
                #pat_obj = visit_obj.patient_detail
            #except (VisitDetail.DoesNotExist, ValueError, NameError, AttributeError, KeyError, TypeError):
                #raise Http404(" ERROR! Bad Request Attributes. Please retry.")
        #if request.method == 'GET' and request.is_ajax():
            #phyexam_obj = PhyExam(visit_detail=visit_obj)
            #phyexam_form = OP_PhyExamForm(instance=phyexam_obj)
            #variable = RequestContext(request, {'user': user,
                                                #'pat_obj': pat_obj,
                                                #'visit_obj': visit_obj,
                                                #'phyexam_obj': phyexam_obj,
                                                #'phyexam_form': phyexam_form
                                                #})
            #return render_to_response('phyexam/visit/add.html', variable)
        #if request.method == 'POST' and request.is_ajax():
            #phyexam_obj = PhyExam(visit_detail=visit_obj)
            #phyexam_form = OP_PhyExamForm(request.POST, instance=phyexam_obj)
            #if phyexam_form.is_valid():
                #saved_phyexam = phyexam_form.save()
                #success = True
                #error_message = "Physical Examination Saved Successfully"
                #form_errors = None
            #else:
                #success = False
                #error_message = "ERROR! Physical examination form couls not be saved"
                #form_errors = phyexam_form.errors
            #data = {'success': success, 'error_message': error_message, 'form_errors':
                    #form_errors}
            #json = simplejson.dumps(data)
            #return HttpResponse(json, content_type='application/json')
        #else:
            #raise Http404("Bad Request / Request method")
    #else:
        #return HttpResponseRedirect(settings.LOGIN_URL)


#@login_required
#def phyexam_edit(request, id=None):
    #if request.user:
        #user = request.user
        #if id:
            #try:
                #id = int(id)
                #phyexam_obj = PhyExam.objects.get(pk=id)
        #else:
            #try:
                #id = int(request.GET.get('visit_id'))
                #phyexam_obj = PhyExam.objects.get(pk=id)
            #except (PhyExam.DoesNotExist, ValueError, NameError, AttributeError, KeyError, TypeError):
                #raise Http404(" ERROR! Bad Request Attributes. Please retry.")
        #if request.method == 'GET' and request.is_ajax():
            #phyexam_form = OP_PhyExamForm(instance=phyexam_obj)
            #variable = RequestContext(request, {'user': user,
                                                #'pat_obj': phyexam_obj.visit_detail.patient_detail,
                                                #'visit_obj': phyexam_obj.visit_detail,
                                                #'phyexam_obj': phyexam_obj,
                                                #'phyexam_form': phyexam_form
                                                #})
            #return render_to_response('phyexam/visit/edit.html', variable)
        #if request.method == 'POST' and request.is_ajax():
            #phyexam_form = OP_PhyExamForm(request.POST, instance=phyexam_obj)
            #if phyexam_form.is_valid():
                #saved_phyexam = phyexam_form.save()
                #success = True
                #error_message = "Physical Examination Saved Successfully"
                #form_errors = None
            #else:
                #success = False
                #error_message = "ERROR! Physical examination form couls not be saved"
                #form_errors = phyexam_form.errors
            #data = {'success': success, 'error_message': error_message, 'form_errors':
                    #form_errors}
            #json = simplejson.dumps(data)
            #return HttpResponse(json, content_type='application/json')
        #else:
            #raise Http404("Bad Request / Request method")
    #else:
        #return HttpResponseRedirect(settings.LOGIN_URL)


#@login_required
#def phyexam_del(request, id=None):

    #if request.user:
        #user = request.user

        #if user.is_superuser:

            #if id:
                #try:
                    #id = int(id)
                    #phyexam_obj = PhyExam.objects.get(pk=id)
            #else:
                #try:
                    #id = int(request.GET.get('visit_id'))
                    #phyexam_obj = PhyExam.objects.get(pk=id)
                #except (PhyExam.DoesNotExist, ValueError, NameError, AttributeError, KeyError, TypeError):
                    #raise Http404(
                        #" ERROR! Bad Request Attributes. Please retry.")

            #if request.method == 'GET' and request.is_ajax():
                #phyexam_obj.delete()
                #success = True
                #error_message = "Physical Examination Deleted Successfully"
                #form_errors = None
                #data = {'success': success, 'error_message': error_message, 'form_errors':
                        #form_errors}
                #json = simplejson.dumps(data)
                #return HttpResponse(json, content_type='application/json')
            #else:
                #raise Http404("Bad Request / Request method")

        #else:
            #success = False
            #error_message = "ERROR! Permission Denied"
            #form_errors = None
            #data = {'success': success, 'error_message': error_message, 'form_errors':
                    #form_errors}
            #json = simplejson.dumps(data)
            #return HttpResponse(json, content_type='application/json')

    #else:
        #return HttpResponseRedirect(settings.LOGIN_URL)


#@login_required
#def phyexam_home(request, id, ip_or_op='ip'):
    #"""View listing all the physical examinations for that admission Takes
    #admission id as the argument."""
    #if request.user:
        #user = request.user
        #if ip_or_op == "ip":
            #status = ip_or_op
            #if request.method == "GET":
    #try:
        #id = int(id)
        #adm_obj = Admission.objects.get(pk=id)
    #except (ValueError, TypeError, AttributeError, Admission.DoesNotExist):
        #raise Http404("Bad Request")
    #phyexam_objs = PhyExam.objects.filter(admission_detail=adm_obj)
    #if phyexam_objs:
        #reg_list = []
        #for phyexam_obj in phyexam_objs:
            #vital_objs = Vital.objects.filter(phyexam=phyexam_obj)
            #gen_exam_objs = GenExam.objects.filter(phyexam=phyexam_obj)
            #sys_exam_objs = SysExam.objects.filter(phyexam=phyexam_obj)
            #reg_exam_objs = RegExam.objects.filter(phyexam=phyexam_obj)
            #for reg_exam in reg_exam_objs:
                #if reg_exam.phyexam == phyexam_obj:
        #reg_match = {phyexam_obj: reg_exam}
        #reg_list.append(reg_match)
            #else:
        #reg_match = {phyexam_obj: None}
        #reg_list.append(reg_match)

            #peri_neuro_exam_objs = PeriNeuroExam.objects.filter(
                #phyexam=phyexam_obj)
            #vasc_exam_objs = VascExam.objects.filter(phyexam=phyexam_obj)
        #exam_object_list = [vital_objs, gen_exam_objs, sys_exam_objs,
                            #reg_exam_objs, peri_neuro_exam_objs, vasc_exam_objs
                            #]
    #else:
        #raise Http404("Bad Request:: The requested PhyExam DoesNotExist")
    #for objects in exam_object_list:
        #if objects == None:
            #objects.remove()
    #variable = RequestContext(request, {'user': user, 'adm_obj': adm_obj,
                                        #'phyexam_objs': phyexam_objs,
                                        #'exam_object_list': exam_object_list,
                                        #'vital_objs': vital_objs,
                                        #'gen_exam_objs': gen_exam_objs,
                                        #'sys_exam_objs': sys_exam_objs,
                                        #'reg_exam_objs': reg_exam_objs,
                                        #'peri_neuro_exam_objs': peri_neuro_exam_objs,
                                        #'vasc_exam_objs': vasc_exam_objs,
                                        #'adm_obj': adm_obj,
                                        #'reg_list': reg_list,
                                        #'status': status,
                                        #})
    #return render_to_response('phyexam/phyexam_home.html', variable)
        #else:
    #raise Http404("Bad Request:: " + str(request.method))

        #elif ip_or_op == 'op':
            #status = ip_or_op
            #if request.method == "GET":
    #try:
        #id = int(id)
        #visit_obj = VisitDetail.objects.get(pk=id)
    #except (ValueError, TypeError, AttributeError, VisitDetail.DoesNotExist):
        #raise Http404("Bad Request")
    #phyexam_objs = PhyExam.objects.filter(visit_detail=visit_obj)
    #if phyexam_objs:
        #reg_list = []
        #for phyexam_obj in phyexam_objs:
            #vital_objs = Vital.objects.filter(phyexam=phyexam_obj)
            #gen_exam_objs = GenExam.objects.filter(phyexam=phyexam_obj)
            #sys_exam_objs = SysExam.objects.filter(phyexam=phyexam_obj)
            #reg_exam_objs = RegExam.objects.filter(phyexam=phyexam_obj)
            #for reg_exam in reg_exam_objs:
                #if reg_exam.phyexam == phyexam_obj:
        #reg_match = {phyexam_obj: reg_exam}
        #reg_list.append(reg_match)
            #else:
        #reg_match = {phyexam_obj: None}
        #reg_list.append(reg_match)
            #peri_neuro_exam_objs = PeriNeuroExam.objects.filter(
                #phyexam=phyexam_obj)
            #vasc_exam_objs = VascExam.objects.filter(phyexam=phyexam_obj)
        #exam_object_list = [vital_objs, gen_exam_objs, sys_exam_objs,
                            #reg_exam_objs, peri_neuro_exam_objs, vasc_exam_objs
                            #]
    #else:
        #raise Http404("Bad Request:: The requested PhyExam DoesNotExist")
    #for objects in exam_object_list:
        #if objects == None:
            #objects.remove()
    #variable = RequestContext(request, {'user': user, 'visit_obj': visit_obj,
                                        #'phyexam_objs': phyexam_objs,
                                        #'exam_object_list': exam_object_list,
                                        #'vital_objs': vital_objs,
                                        #'gen_exam_objs': gen_exam_objs,
                                        #'sys_exam_objs': sys_exam_objs,
                                        #'reg_exam_objs': reg_exam_objs,
                                        #'peri_neuro_exam_objs': peri_neuro_exam_objs,
                                        #'vasc_exam_objs': vasc_exam_objs,
                                        ##'visit_objs':adm_obj,
                                        #'reg_list': reg_list,
                                        #'status': status,
                                        #})
    #return render_to_response('phyexam/phyexam_home_op.html', variable)
        #else:
    #raise Http404("Bad Request:: " + str(request.method))
    #else:
        #raise Http404("User not logged in")


#@login_required
#def start_phyexam(request, id, consult_nature='start', ip_or_op='ip'):
    #"""View starting the physical examination of an admission with vitals,
    #general and systemic exams.

    #Takes admission id as the argument. Next view will handle the
    #regional orthopaedic exam.

    #"""
    #if request.user:
        #user = request.user
        #if ip_or_op == 'ip':
            #if request.method == "GET":
                #try:
                    #id = int(id)
                    #adm_obj = Admission.objects.get(pk=id)
                #except(TypeError, ValueError, AttributeError, Admission.DoesNotExist):
                    #raise Http404(
                        #"ValueError / AttributeError/ TypeError / The Data does not exist")
                #print request.GET.getlist('exam_choice')
                #forms_requested = request.GET.getlist('exam_choice')
                #forms_to_render = []
                #print forms_requested
                #phyexams_for_pat = PhyExam.objects.filter(
                    #admission_detail=adm_obj)
                #if not phyexams_for_pat and consult_nature == 'start':
                    #phyexam_obj = PhyExam(
                        #admission_detail=adm_obj, consult_nature='Initial-IP')
                    #phyexam_form = IP_Initial_PhyExamForm(
                        #instance=phyexam_obj)
                #elif phyexams_for_pat:
                    #if consult_nature == 'fu':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Follow Up-IP')
                    #elif consult_nature == 'preop':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Pre-Op-IP')
                    #elif consult_nature == 'postop':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Post-Op-IP')
                    #elif consult_nature == 'dis':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Dis-IP')
                    #else:
                        #raise Http404('Please check the request..')
                    #phyexam_form = IP_Initial_PhyExamForm(
                        #instance=phyexam_obj)
                #error_message = ""
                #variable_dict = {'user': user,
                                 #'phyexam_obj': phyexam_obj,
                                 #'phyexam_form': phyexam_form,
                                 #'adm_obj': adm_obj,
                                 #'error_message': error_message,
                                 #'consult_nature': consult_nature
                                 #}
                #if 'vital' in forms_requested:
                    #vital_obj = Vital(phyexam=phyexam_obj)
                    #vital_form = VitalForm(instance=vital_obj)
                    #variable_dict['vital_form'] = vital_form
                #if 'gen' in forms_requested:
                    #gen_exam_obj = GenExam(phyexam=phyexam_obj)
                    #gen_exam_form = GenExamForm(instance=gen_exam_obj)
                    #variable_dict['gen_exam_form'] = gen_exam_form
                #if 'sys' in forms_requested:
                    #sys_exam_obj = SysExam(phyexam=phyexam_obj)
                    #sys_exam_form = SysExamForm(instance=sys_exam_obj)
                    #variable_dict['sys_exam_form'] = sys_exam_form
                #if 'reg' in forms_requested:
                    #reg_exam_obj = RegExam(phyexam=phyexam_obj)
                    #reg_exam_form = RegExamForm(instance=reg_exam_obj)
                    #variable_dict['reg_exam_form'] = reg_exam_form
                #if 'neuro' in forms_requested:
                    #neuro_exam_obj = PeriNeuroExam(phyexam=phyexam_obj)
                    #neuro_exam_form = PeriNeuroExamForm(
                        #instance=neuro_exam_obj)
                    #variable_dict['neuro_exam_form'] = neuro_exam_form
                #if 'vasc' in forms_requested:
                    #vasc_exam_obj = VascExam(phyexam=phyexam_obj)
                    #vasc_exam_form = VascExamForm(instance=vasc_exam_obj)
                    #variable_dict['vasc_exam_form'] = vasc_exam_form
                #variable = RequestContext(request, variable_dict)
                #if adm_obj.admission_closed == False:
                    #print 'printing variable dict: '
                    #print variable_dict.keys()
                    #return render_to_response('phyexam/phyexam_start.html', variable)
                #else:
                    #error_message += "The admission is closed. you cannot add further medical examinations."
                    #variable = RequestContext(request, variable_dict)
                    #return render_to_response('phyexam/phyexam_home.html', variable)

            #elif request.method == "POST":
                #print request.POST
                #try:
                    #id = int(id)
                    #adm_obj = Admission.objects.get(pk=id)
                #except(TypeError, ValueError, AttributeError, Admission.DoesNotExist):
                    #raise Http404(
                        #"ValueError / AttributeError/ TypeError / The Data does not exist")
                #phyexams_for_pat = PhyExam.objects.filter(
                    #admission_detail=adm_obj)
                #if not phyexams_for_pat:
                    #phyexam_obj = PhyExam(
                        #admission_detail=adm_obj, consult_nature='Initial-IP')
                    #phyexam_form = IP_Initial_PhyExamForm(
                        #request.POST, instance=phyexam_obj)
                #elif phyexams_for_pat:
                    #if consult_nature == 'fu':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Follow Up-IP')
                    #elif consult_nature == 'preop':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Pre-Op-IP')
                    #elif consult_nature == 'postop':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Post-Op-IP')
                    #elif consult_nature == 'dis':
                        #phyexam_obj = PhyExam(
                            #admission_detail=adm_obj, consult_nature='Dis-IP')
                    #else:
                        #raise Http404('Please check the request..')
                    #phyexam_form = IP_Initial_PhyExamForm(
                        #request.POST, instance=phyexam_obj)
                #forms_to_validate = []
                #vital_form = ''
                #gen_exam_form = ''
                #sys_exam_form = ''
                #reg_exam_form = ''
                #neuro_exam_form = ''
                #vasc_exam_form = ''
                #if request.POST.get('vital'):
                    #vital_obj = Vital(phyexam=phyexam_obj)
                    #vital_form = VitalForm(
                        #request.POST, instance=vital_obj)
                    #forms_to_validate.append(vital_form)
                #if request.POST.get('gen'):
                    #gen_exam_obj = GenExam(phyexam=phyexam_obj)
                    #gen_exam_form = GenExamForm(
                        #request.POST, instance=gen_exam_obj)
                    #forms_to_validate.append(gen_exam_form)
                #if request.POST.get('sys'):
                    #sys_exam_obj = SysExam(phyexam=phyexam_obj)
                    #sys_exam_form = SysExamForm(
                        #request.POST, instance=sys_exam_obj)
                    #forms_to_validate.append(sys_exam_form)
                #if request.POST.get('reg'):
                    #reg_exam_obj = RegExam(phyexam=phyexam_obj)
                    #reg_exam_form = RegExamForm(
                        #request.POST, instance=reg_exam_obj)
                    #forms_to_validate.append(reg_exam_form)
                #if request.POST.get('neuro'):
                    #neuro_exam_obj = PeriNeuroExam(phyexam=phyexam_obj)
                    #neuro_exam_form = PeriNeuroExamForm(
                        #request.POST, instance=neuro_exam_obj)
                    #forms_to_validate.append(neuro_exam_form)
                #if request.POST.get('vasc'):
                    #vasc_exam_obj = VascExam(phyexam=phyexam_obj)
                    #vasc_exam_form = VascExamForm(
                        #request.POST, instance=vasc_exam_obj)
                    #forms_to_validate.append(vasc_exam_form)
                #data = {'phyexam': phyexam_obj}
                #form_errors = []
## FIXME: VALIDATION TO BE HANDLED...
                #if phyexam_form.is_valid() and all([form.is_valid() for form in forms_to_validate]):
                    #print 'evaluating phyexam_form'
                    #saved_phyexam = phyexam_form.save()
                    #for form in forms_to_validate:
                        #saved_form = form.save()
                        #saved_form.phyexam = saved_phyexam
                        #saved_form.save()
                        #form_errors.append(form.errors)
                        #if vital_form in forms_to_validate:
                            #saved_phyexam.has_vital = True
                        #if gen_exam_form in forms_to_validate:
                            #saved_phyexam.has_gen = True
                        #if sys_exam_form in forms_to_validate:
                            #saved_phyexam.has_sys = True
                        #if reg_exam_form in forms_to_validate:
                            #saved_phyexam.has_reg = True
                        #if neuro_exam_form in forms_to_validate:
                            #saved_phyexam.has_neuro = True
                        #if vasc_exam_form in forms_to_validate:
                            #saved_phyexam.has_vasc = True
                        #saved_phyexam.save()
                    #success = True
                    #error_message = 'Forms saved successfully.'
                    #data = {'success': success, 'error_message': error_message, 'form_errors':
                            #form_errors}
                    #json = simplejson.dumps(data)
                    #return HttpResponse(json, content_type='application/json')
                #else:
                    #success = False
                    #error_message = "Please correct errors ! "
                    #data = {'success': success, 'error_message': error_message, 'form_errors':
                            #form_errors}
                    #json = simplejson.dumps(data)
                    #return HttpResponse(json, content_type='application/json')
            #else:
                #raise Http404("Bad / Unknown Request:: " + str(
                    #request.method) + ' / OR this is a Non- Ajax request. ')

        #if ip_or_op == 'op':
            #if request.method == "GET":
                #try:
                    #id = int(id)
                    #visit_obj = VisitDetail.objects.get(pk=id)
                #except(TypeError, ValueError, AttributeError, VisitDetail.DoesNotExist):
                    #raise Http404(
                        #"ValueError / AttributeError/ TypeError / The Data does not exist")
                ## define all the objects for physical exam::
                #phyexams_for_pat = PhyExam.objects.filter(
                    #visit_detail=visit_obj)
                #if not phyexams_for_pat:
                ## define all the objects for physical exam::
                    #phyexam_obj = PhyExam(
                        #visit_detail=visit_obj, consult_nature='Initial-OP')
                    #phyexam_form = OP_Initial_PhyExamForm(
                        #instance=phyexam_obj)
                #elif phyexams_for_pat:
                    #if consult_nature == 'fu':
                    ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Follow Up-OP')
                    #elif consult_nature == 'preop':
                        ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Pre-Op-OP')
                    #elif consult_nature == 'postop':
                        ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Post-Op-OP')
                    #elif consult_nature == 'dis':
                        ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Dis-OP')
                    #else:
                        #raise Http404('Please check the request..')
                    #phyexam_form = OP_Initial_PhyExamForm(
                        #request.POST, instance=phyexam_obj)
                #vital_obj = Vital(phyexam=phyexam_obj)
                #gen_exam_obj = GenExam(phyexam=phyexam_obj)
                #sys_exam_obj = SysExam(phyexam=phyexam_obj)
                ## define all the forms::
                #error_message = ""
                #vital_form = OP_VitalForm(instance=vital_obj)
                #gen_exam_form = OP_GenExamForm(instance=gen_exam_obj)
                #sys_exam_form = OP_SysExamForm(instance=sys_exam_obj)
                #variable = RequestContext(request, {'user': user,
                                                    #'phyexam_obj': phyexam_obj,
                                                    #'phyexam_form': phyexam_form,
                                                    #'sys_exam_form': sys_exam_form,
                                                    #'gen_exam_form': gen_exam_form,
                                                    #'vital_form': vital_form,
                                                    #'visit_obj': visit_obj,
                                                    #'error_message': error_message,
                                                    #'consult_nature': consult_nature
                                                    #})
                #if not visit_obj.is_visit_active == False:
                    #return render_to_response('phyexam/phyexam_start_op.html', variable)
                #else:
                    #error_message = "The Visit is closed. you cannot add further medical examinations."
                    #return render_to_response('phyexam/phyexam_home_op.html', variable)
            #elif request.method == "POST":
                #try:
                    #id = int(id)
                    #visit_obj = VisitDetail.objects.get(pk=id)
                #except(TypeError, ValueError, AttributeError, VisitDetail.DoesNotExist):
                    #raise Http404(
                        #"ValueError / AttributeError/ TypeError / The Data does not exist")
                ## define all the objects for physical exam::
                ## define all the objects for physical exam::
                #phyexams_for_pat = PhyExam.objects.filter(
                    #visit_detail=visit_obj)
                #if not phyexams_for_pat:
                ## define all the objects for physical exam::
                    #phyexam_obj = PhyExam(
                        #visit_detail=visit_obj, consult_nature='Initial-OP')
                    #phyexam_form = OP_Initial_PhyExamForm(
                        #request.POST, instance=phyexam_obj)
                #elif phyexams_for_pat:
                    #if consult_nature == 'fu':
                    ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Follow Up-OP')
                    #elif consult_nature == 'preop':
                        ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Pre-Op-OP')
                    #elif consult_nature == 'postop':
                        ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Post-Op-OP')
                    #elif consult_nature == 'dis':
                        ## define all the objects for physical exam::
                        #phyexam_obj = PhyExam(
                            #visit_detail=visit_obj, consult_nature='Dis-OP')
                    #else:
                        #raise Http404('Please check the request..')
                    #phyexam_form = OP_Initial_PhyExamForm(
                        #request.POST, instance=phyexam_obj)
                #vital_obj = Vital(phyexam=phyexam_obj)
                #gen_exam_obj = GenExam(phyexam=phyexam_obj)
                #sys_exam_obj = SysExam(phyexam=phyexam_obj)
                ## define all the forms::
                #data = {'phyexam': phyexam_obj}
                #vital_form = OP_VitalForm(
                    #request.POST, data, instance=vital_obj)
                #gen_exam_form = OP_GenExamForm(
                    #request.POST, data, instance=gen_exam_obj)
                #sys_exam_form = OP_SysExamForm(
                    #request.POST, data, instance=sys_exam_obj)
                ## validate all the forms and save them
                #if phyexam_form.is_valid() and  vital_form.is_valid() and \
                    #sys_exam_form.is_valid() and gen_exam_form.is_valid():
                    #phyexam_save = phyexam_form.save()
                    ##vital_form.cleaned_data['phyexam'] = phyexam_save
                    #vital_save = vital_form.save()
                    #vital_save.phyexam = phyexam_save
                    #vital_save.save()
                    #vital_form.save()
                    #gen_exam_save = gen_exam_form.save()
                    #gen_exam_save.phyexam = phyexam_save
                    #gen_exam_save.save()
                    #sys_exam_save = sys_exam_form.save()
                    #sys_exam_save.phyexam = phyexam_save
                    #sys_exam_save.save()
                    #phyexam_save.has_others(phyexam_save.id)
                    #phyexam_save.save()
                    ## redirect to home url of the phyexam if all is well.
                    #return HttpResponseRedirect('/phyexam/home/' + str(id) + '/op/')
                #else:
                ## else raise the error message and return the form
                    #error_message = "There were error and forms were not saved"
                    #variable = RequestContext(request, {'user': user,
                                                        #'phyexam_form': phyexam_form,
                                                        #'sys_exam_form': sys_exam_form,
                                                        #'gen_exam_form': gen_exam_form,
                                                        #'vital_form': vital_form,
                                                        #'error_message': error_message,
                                                        #'visit_obj': visit_obj,
                                                        #'consult_nature': consult_nature,
                                                        #}
                                              #)
                    #return render_to_response('phyexam/phyexam_start_op.html', variable)
            #else:
                #raise Http404("Bad / Unknown Request:: " + str(request.method))
    #else:
        #raise Http404("Bad Request:: User Not Logged in")


#@login_required
#def add_other_exams(request, id, ip_or_op='ip'):
    #if request.user:
        #user = request.user
        #try:
            #id = int(id)
            #phyexam_obj = PhyExam.objects.get(pk=id)
        #except (ValueError, AttributeError, TypeError, PhyExam.DoesNotExist):
            #raise Http404("Bad Request:: Error Occured / Data Does Not Exist")
        #reg_exam_obj = RegExam(phyexam=phyexam_obj)
        #peri_neuro_exam_obj = PeriNeuroExam(phyexam=phyexam_obj)
        #vasc_exam_obj = VascExam(phyexam=phyexam_obj)
        #other_forms = ""
        #if ip_or_op == 'ip':
            #status = 'ip'
        #elif ip_or_op == 'op':
            #status = 'op'
        #if request.method == "GET":
            #form_list = []
            #form_dict = {}
            #if 'reg_exam_form' in request.GET:
                #reg_exam_form = RegExamForm(instance=reg_exam_obj)
                #form_dict['reg_exam_form'] = reg_exam_form
                #other_forms = '''
                      #<select id="reg_exam_choice" multiple = "true" title = "Ctrl + Click to select more than one">
                        #<option value="cspine" id = 'cspine'>             Cervical Spine </option>
                        #<option value="lspine" id = 'lspine'>             Thoracic and Lumbar Spine </option>
                        #<option value="shoulder_and_arm" id = 'shoulder_and_arm'> Shoulder and Arm </option>
                        #<option value="elbow_and_forearm" id = 'elbow_and_forearm'>   Elbow and Forearm </option>
                        #<option value="wrist_and_hand" id = 'wrist_and_hand'>       Wrist and Hand </option>
                        #<option value="hip_and_thigh" id = 'hip_and_thigh'>           Hip and Thigh </option>
                        #<option value="knee_and_leg" id = 'knee_and_leg'>         Knee and Leg </option>
                        #<option value="ankle_and_foot" id = "ankle_and_foot">       Ankle and Foot </option>
                      #</select>
                      #'''
            #if 'neuro_exam_form' in request.GET:
                #neuro_exam_form = PeriNeuroExamForm(
                    #instance=peri_neuro_exam_obj)
                #form_dict['neuro_exam_form'] = neuro_exam_form
            #if 'vasc_exam_form' in request.GET:
                #vasc_exam_form = VascExamForm(instance=vasc_exam_obj)
                #form_dict['vasc_exam_form'] = vasc_exam_form
            #if len(form_dict.keys()) == 0:
                #if ip_or_op == 'ip':
                    #return HttpResponseRedirect('/phyexam/home/' + str(phyexam_obj.admission_detail.id) + '/' + str(status) + '/')
                #elif ip_or_op == 'op':
                    #return HttpResponseRedirect('/phyexam/home/' + str(phyexam_obj.visit_detail.id) + '/' + str(status) + '/')
            #variable = RequestContext(request, {'user': user,
                                                #'phyexam_obj': phyexam_obj,
                                                #'form_dict': form_dict,
                                                #'other_forms': other_forms,
                                                #'status': status,
                                                #})
            #return render_to_response('phyexam/add_other_exams.html', variable)
        #elif request.method == "POST":
            #form_list = []
            #form_dict = {}
            #if 'reg_exam_form' in request.POST:
                #reg_exam_form = RegExamForm(
                    #request.POST, instance=reg_exam_obj)
                #form_dict['reg_exam_form'] = reg_exam_form
            #if 'neuro_exam_form' in request.POST:
                #neuro_exam_form = PeriNeuroExamForm(
                    #request.POST, instance=peri_neuro_exam_obj)
                #form_dict['neuro_exam_form'] = neuro_exam_form
            #if 'vasc_exam_form' in request.POST:
                #vasc_exam_form = VascExamForm(
                    #request.POST, instance=vasc_exam_obj)
                #form_dict['vasc_exam_form'] = vasc_exam_form
            #if len(form_dict.keys()) == 0:
                #if ip_or_op == 'ip':
                    #return HttpResponseRedirect('/phyexam/home/' + str(phyexam_obj.admission_detail.id) + '/' + str(status) + '/')
                #elif ip_or_op == 'op':
                    #return HttpResponseRedirect('/phyexam/home/' + str(phyexam_obj.visit_detail.id) + '/' + str(status) + '/')
            #saved_obj = []
            #for forms in form_dict.values():
                #if forms.is_valid():
                    #save_obj = forms.save()
                    #save_obj.phyexam.has_others(id)
                    #phyexam_obj.save()
                    #saved_obj.append(forms)
                    #if len(saved_obj) == len(form_dict.values()):
                        #if ip_or_op == 'ip':
                            #return HttpResponseRedirect('/phyexam/home/' + str(phyexam_obj.admission_detail.id) + '/' + str(status) + '/')
                        #elif ip_or_op == 'op':
                            #return HttpResponseRedirect('/phyexam/home/' + str(phyexam_obj.visit_detail.id) + '/' + str(status) + '/')
                #else:
                    #variable = RequestContext(request, {'user': user,
                                                        #'form_dict': form_dict,
                                                        #'phyexam_obj': phyexam_obj,
                                                        #'status': status,
                                                        #})
                    #return render_to_response('phyexam/add_other_exams.html', variable)
        #else:
            #raise Http404("Bad Request:: " + str(request.method))
    #else:
        #user = "Anonymous User"
        #raise Http404("Bad Request:: " + user + "- Please Log in")


#@login_required
#def phyexam_edit_del(request, id, request_object='whole', action='edit'):
    #if request.user:
        #user = request.user
        #object_list = ['whole', 'vital', 'gen',
                       #'sys', 'reg', 'neuro', 'vasc', 'main']
        #object_dict = {'vital': Vital, 'gen': GenExam, 'reg': RegExam, 'sys':
                       #SysExam, 'neuro': PeriNeuroExam, 'vasc': VascExam, 'main': PhyExam}
        #model_form_match = {PhyExam: PhyExamForm, SysExam: SysExamForm,
                            #Vital: VitalForm, GenExam: GenExamForm,
                            #RegExam: RegExamForm,
                            #PeriNeuroExam: PeriNeuroExamForm,
                            #VascExam: VascExamForm, }
        #if request_object in object_list:
            #if request.method == 'GET' and request_object == "whole":
    #try:
        #id = int(id)
        #phyexam_obj = PhyExam.objects.get(pk=id)
        #adm_obj = phyexam_obj.admission_detail
    #except (PhyExam.DoesNotExist, ValueError, AttributeError, TypeError):
        #raise Http404("Bad Request:: Error / Data does not exist")

    #if action == "add":
        #return HttpResponseRedirect('/phyexam/start/' + str(adm_obj.id))
    #elif action == "edit":
        #vital_objs = Vital.objects.filter(phyexam=phyexam_obj)
        #gen_objs = GenExam.objects.filter(phyexam=phyexam_obj)
        #sys_objs = SysExam.objects.filter(phyexam=phyexam_obj)
        #reg_objs = RegExam.objects.filter(phyexam=phyexam_obj)
        #neuro_objs = PeriNeuroExam.objects.filter(phyexam=phyexam_obj)
        #vasc_objs = VascExam.objects.filter(phyexam=phyexam_obj)
        #variable = RequestContext(request, {'user': user,
                                            #'phyexam_obj': phyexam_obj,
                                            #'vital_objs': vital_objs,
                                            #'gen_objs': gen_objs,
                                            #'sys_objs': sys_objs,
                                            #'reg_objs': reg_objs,
                                            #'neuro_objs': neuro_objs,
                                            #'vasc_objs': vasc_objs, 'adm_obj': adm_obj})
        #return render_to_response('phyexam/edit_phyexam_whole.html', variable)

    #elif action == "del":
        #if user.is_staff:
            #phyexam_obj.delete()
            #return HttpResponseRedirect('/phyexam/home/' + str(adm_obj.id) + "/")
        #else:
            #raise Http404(
                #"Bad Request:: User should be logged in and should be staff to delete")
    #else:
        #raise Http404("Bad Request:: " + str(action))

            #elif request_object in ['vital', 'gen', 'sys', 'reg', 'neuro', 'vasc', 'main']:

    #request_model = object_dict[request_object]
    #request_form = model_form_match[request_model]
    #try:
        #id = int(id)
        #action_obj = request_model.objects.get(pk=id)
        #phyexam_obj = action_obj.phyexam
        #adm_obj = phyexam_obj.admission_detail
    #except (request_model.DoesNotExist, ValueError, AttributeError, TypeError):
        #raise Http404("Bad Request:: Error / Data does not exist")

    #if action == "edit":
        #action = "/phyexam/" + \
            #str(request_object) + "/" + str(
                #action) + '/' + str(action_obj.id) + '/'
        #button = "Edit"
        #if request.method == 'GET':
            #form = request_form(instance=action_obj)
            #variable = RequestContext(
                #request, {'user': user, 'action_obj': action_obj,
                          #'action': action, 'button': button,
                          #'form': form, 'adm_obj': adm_obj})
            #return render_to_response('phyexam/edit_phyexam_part.html', variable)
        #elif request.method == "POST":
            #form = request_form(request.POST, instance=action_obj)
            #if form.is_valid():
                #save_action_obj = form.save()
                #return HttpResponseRedirect('/phyexam/whole/edit/' + str(phyexam_obj.id) + '/')
            #else:
                #variable = RequestContext(
                    #request, {'user': user, 'action_obj': action_obj,
                              #'action': action, 'button': button,
                              #'form': form, 'adm_obj': adm_obj})
                #return render_to_response('phyexam/edit_phyexam_part.html', variable)
        #else:
            #raise Http404("Bad Request:: " + request.method)

    #elif action == "del":
        #if request.method == 'GET' and user.is_staff:
            #action_obj.delete()
            #phyexam_obj.has_others(phyexam_obj.id)
            #return HttpResponseRedirect('/phyexam/whole/edit/' + str(phyexam_obj.id) + '/')
        #else:
            #raise Http404("Bad Request or User is not staff")
    #else:
        #raise Http404("ERROR:: Unknown Action Requested:: " + str(action))
            #else:
    #raise Http404("ERROR:: Unknown Object Requested:: " + str(request_object))
    #else:
        #user = "Anonymous User"
        #raise Http404("Bad Request:: " + user)
