#################################################################################
# Project     : AuShadha
# Description : AuShadha Views for OPD Visits History
# Author      : Dr.Easwar T.R 
# Date        : 27-12-2012
# License     : GNU - GPL Version 3, see AuShadha/LICENSE.txt
#################################################################################


# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
#from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator
from django.utils import simplejson

# General Module imports-----------------------------------
from datetime import datetime, date, time
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from collections import OrderedDict
import importlib

# Application Specific Model Imports-----------------------
from AuShadha.utilities.forms import AuModelFormErrorFormatter, aumodelformerrorformatter_factory
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.aushadha_users.models import AuShadhaUser
from AuShadha.apps.clinic.models import Clinic, Staff
from AuShadha.apps.ui.ui import ui as UI

from registry.inv_and_imaging.models import LabInvestigationRegistry, ImagingInvestigationRegistry

#from patient.models import PatientDetail
#from admission.models import AdmissionDetail
PatientDetail = UI.get_module('PatientRegistration')
AdmissionDetail = UI.get_module('Admission')
VisitDetail = UI.get_module('OPD_Visit')

from .models import VisitAssessmentAndPlan, VisitAssessmentAndPlanForm


# views start here;;

@login_required
def visit_assessment_and_plan_template(request, assessment_name, visit_id = None):

    if request.method == "GET":
        user = request.user

        try:
            if visit_id:
                visit_id = int( visit_id )

            else:
                visit_id = int( request.GET.get('visit_id') )

            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            exam_class = EXAM_NAME_MODEL_MAP.get(assessment_name,'')

            if not exam_class:
                raise Http404("Invalid Exam Requested")

            try:
                template_file = 'visit_assessment_and_plan/%s/template.html' %(assessment_name)
                #template = loader.get_template(template_file)
                variable = RequestContext(request, {'user': user,
                                                    'assessment_name': assessment_name ,
                                                    'visit_detail_obj': visit_detail_obj
                                                    })
                #rendered_html = template.render(variable)
                return render_to_response(template_file, variable )

            except Exception as ex:
                raise Http404("ERROR! " , ex)


        except (ValueError, KeyError, NameError, AttributeError):
            raise Http404("Invalid Exam template. ")

    else:
        raise Http404("Bad Request Method")


@login_required
def get_visit_assessment_and_plan(request, visit_id = None):

    if request.method == 'GET':
        user = request.user
        try:
            if visit_id:
                visit_id = int(visit_id)
            else:
                visit_id = int(request.GET.get('visit_id'))

            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            patient_detail_obj = visit_detail_obj.patient_detail

            if not getattr(visit_detail_obj, 'urls', None):
                visit_detail_obj.save()

        except(AttributeError, NameError, TypeError, ValueError, KeyError):
            raise Http404("ERROR:: Bad request.Invalid arguments passed")

        except(VisitDetail.DoesNotExist):
            raise Http404("ERROR:: Patient requested does not exist.")

        data = []
        for visit in VisitDetail.objects.filter(patient_detail = patient_detail_obj):
            if visit != visit_detail_obj:
                visit_assessment_and_plan_obj = VisitAssessmentAndPlan.objects.filter(visit_detail = visit)
                if visit_assessment_and_plan_obj:
                    data.append(visit_assessment_and_plan_obj[0])

        if data:
            for assessment_and_plan in data:
                if not getattr(assessment_and_plan, 'urls', None):
                    assessment_and_plan.save()

        variable = RequestContext(request, {'user': user, 
                                            'visit_assessment_and_plan_objs': data,
                                            'visit_detail_obj': visit_detail_obj,
                                            'patient_detail_obj': patient_detail_obj
                                            })
        return render_to_response('visit_assessment_and_plan/get_all_visit_assessment_and_plan.html', variable)

    else:
        raise Http404("Bad Request Method")



@login_required
def visit_assessment_and_plan_json(request, visit_id = None):

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))          

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()

    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")

    except(VisitDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")

    #visit_assessment_and_plan_objs  = []
    #all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    #for visit in all_visits:
      #vc = VisitAssessmentAndPlan.objects.filter(visit_detail = visit)
      #for c in vc:
        #visit_assessment_and_plan_objs.append(c)

    visit_assessment_and_plan_objs = VisitAssessmentAndPlan.objects.filter(visit_detail = visit_detail_obj)
    data = []

    if visit_assessment_and_plan_objs:
        for assessment_and_plan in visit_assessment_and_plan_objs:
            if not getattr(assessment_and_plan, 'urls', None):
              assessment_and_plan.save()
            i = 0
            data_to_append = {}
            data_to_append['id'] = assessment_and_plan.id
            data_to_append['possible_diagnosis'] = assessment_and_plan.possible_diagnosis
            data_to_append['case_summary'] = assessment_and_plan.case_summary
            data_to_append['plan'] = assessment_and_plan.plan
            data_to_append['edit'] = assessment_and_plan.urls['edit']
            data_to_append['del'] = assessment_and_plan.urls['del']
            data.append(data_to_append)
            i += 1

    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")



@login_required
def visit_assessment_and_plan_add(request, visit_id = None):

    """ 
    Adds a Visit assessment_and_plan
    """

    user = request.user
    success = False
    error_message = None
    form_errors = []

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(patient_detail_obj, 'urls', None):
          patient_detail_obj.save()

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()

        visit_assessment_and_plan_objs = VisitAssessmentAndPlan.objects.filter(visit_detail = visit_detail_obj)
        if visit_assessment_and_plan_objs:
          return visit_assessment_and_plan_edit(request, visit_assessment_and_plan_id = visit_assessment_and_plan_objs[0].id)

        visit_assessment_and_plan_obj = VisitAssessmentAndPlan(visit_detail=visit_detail_obj)

        if request.method == "GET" and request.is_ajax():

            visit_assessment_and_plan_form = VisitAssessmentAndPlanForm(instance = visit_assessment_and_plan_obj,
                                                      auto_id  = "id_add_visit_assessment_and_plan"+ str(visit_id)+"_%s")
            variable = RequestContext(request, {
                                                'user': user,
                                                'visit_detail_obj': visit_detail_obj,
                                                'visit_assessment_and_plan_form': visit_assessment_and_plan_form,
                                                'patient_detail_obj': patient_detail_obj,
                                                'error_message': error_message,
                                                'success': success,
                                                'visit_assessment_and_plan_action':'add'
                                            })

            return render_to_response('visit_assessment_and_plan/add_or_edit_form.html', variable)

        elif request.method == "POST" and request.is_ajax():

            visit_assessment_and_plan_form = VisitAssessmentAndPlanForm(request.POST, 
                                                                        instance = visit_assessment_and_plan_obj
                                                                        )

            if visit_assessment_and_plan_form.is_valid() :
                saved_visit_assessment_and_plan = visit_assessment_and_plan_form.save(commit=False)
                saved_visit_assessment_and_plan.visit_detail = visit_detail_obj
                saved_visit_assessment_and_plan.save()
                success = True
                error_message = "History Added Successfully"
                redirectUrl = saved_visit_assessment_and_plan.urls['edit']

            else:
                error_message = ''' <h4>
                                      History Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_assessment_and_plan_form)
                error_message += ('\n' + errors)
                redirectUrl = None
                success = False

            data = {'success': success,
                    'error_message': error_message,
                    'redirectUrl': redirectUrl
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")


@login_required
def visit_assessment_and_plan_edit(request, visit_assessment_and_plan_id = None):

    user = request.user
    error_message = None    
    
    try:

        if visit_assessment_and_plan_id:
          visit_assessment_and_plan_id = int(visit_assessment_and_plan_id)

        else:
          visit_assessment_and_plan_id = int(request.GET.get('visit_assessment_and_plan_id'))

        visit_assessment_and_plan_obj = VisitAssessmentAndPlan.objects.get(pk=visit_assessment_and_plan_id)
        visit_detail_obj = visit_assessment_and_plan_obj.visit_detail
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        if not getattr(patient_detail_obj,'urls',None):
          patient_detail_obj.save()

        if not getattr(visit_assessment_and_plan_obj,'urls',None):
          visit_assessment_and_plan_obj.save()

        if request.method == "GET" and request.is_ajax():

            visit_assessment_and_plan_form = VisitAssessmentAndPlanForm(instance = visit_assessment_and_plan_obj, 
                                                                        auto_id = "id_edit_visit_assessment_and_plan"+    str(visit_assessment_and_plan_id)+"_%s"
                                                                        )

            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_assessment_and_plan_obj': visit_assessment_and_plan_obj,
                          'visit_assessment_and_plan_form'  : visit_assessment_and_plan_form  ,
                          'patient_detail_obj': visit_detail_obj.patient_detail,
                          'error_message': error_message,
                          'visit_assessment_and_plan_action':'edit'
                          })

            return render_to_response('visit_assessment_and_plan/add_or_edit_form.html', variable)

        if request.method == "POST" and request.is_ajax():

            visit_assessment_and_plan_form   = VisitAssessmentAndPlanForm(request.POST, 
                                                                          instance = visit_assessment_and_plan_obj 
                                                                          )

            if visit_assessment_and_plan_form.is_valid()    :

                saved_visit_assessment_and_plan = visit_assessment_and_plan_form.save(commit=False)
                saved_visit_assessment_and_plan.visit_detail = visit_detail_obj
                saved_visit_assessment_and_plan.save()
                success = True
                error_message = "Visit Assessment and Plan Edited Successfully"
                redirectUrl = saved_visit_assessment_and_plan.urls['edit']

            else:
                success = False
                error_message = ''' <h4>
                                      Visit Assessment and Plan Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_assessment_and_plan_form)
                error_message += ('\n' + errors)
                redirectUrl = None

            data = {'success': success, 'error_message': error_message , 'redirectUrl': redirectUrl }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
             raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitAssessmentAndPlan.DoesNotExist):
        raise Http404("Requested VisitAssessmentAndPlan Does not exist.")


@login_required
def visit_assessment_and_plan_del(request, visit_assessment_and_plan_id = None):
    
    if request.method == "GET" and request.is_ajax():

        user = request.user

        try:
            if visit_assessment_and_plan_id:
              visit_assessment_and_plan_id = int(visit_assessment_and_plan_id)
            else:
              visit_assessment_and_plan_id = int(request.GET.get('visit_assessment_and_plan_id'))

            visit_assessment_and_plan_obj = VisitAssessmentAndPlan.objects.get(pk=visit_assessment_and_plan_id)
            visit_detail_obj = visit_assessment_and_plan_obj.visit_detail

            if not getattr(visit_detail_obj,'urls', None):
              visit_detail_obj.save()

            visit_assessment_and_plan_obj.delete()
            error_message = None
            success = True
            error_message = "Successfully Deleted Visit Assessment and Plan "
            data = {'success': success, 
                    'error_message': error_message, 
                    'redirectUrl': visit_detail_obj.urls['add']['visit_assessment_and_plan'] 
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitAssessmentAndPlan.DoesNotExist):
            raise Http404("Requested Visit Assessment and Plan Does not exist.")

    else:
        raise Http404(" Error ! Unsupported Request..")