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
import json

# General Module imports-----------------------------------
from datetime import datetime, date, time
#import xhtml2pdf.pisa as pisa
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

from .models import VisitSOAP, VisitSOAPForm


# views start here;;

@login_required
def visit_soap_template(request, soap_name, visit_id = None):

    if request.method == "GET":
        user = request.user

        try:
            if visit_id:
                visit_id = int( visit_id )

            else:
                visit_id = int( request.GET.get('visit_id') )

            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            exam_class = EXAM_NAME_MODEL_MAP.get(soap_name,'')

            if not exam_class:
                raise Http404("Invalid Exam Requested")

            try:
                template_file = 'visit_soap/%s/template.html' %(soap_name)
                #template = loader.get_template(template_file)
                variable = RequestContext(request, {'user': user,
                                                    'soap_name': soap_name ,
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
def get_visit_soap(request, visit_id = None):

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
                visit_soap_obj = VisitSOAP.objects.filter(visit_detail = visit)
                if visit_soap_obj:
                    data.append(visit_soap_obj[0])

        if data:
            for soap in data:
                if not getattr(soap, 'urls', None):
                    soap.save()

        variable = RequestContext(request, {'user': user, 
                                            'visit_soap_objs': data,
                                            'visit_detail_obj': visit_detail_obj,
                                            'patient_detail_obj': patient_detail_obj
                                            })
        return render_to_response('visit_soap/get_all_visit_soap.html', variable)

    else:
        raise Http404("Bad Request Method")



@login_required
def visit_soap_json(request, visit_id = None):

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

    #visit_soap_objs  = []
    #all_visits = VisitDetail.objects.filter(patient_detail = patient_detail_obj)
    #for visit in all_visits:
      #vc = VisitSOAP.objects.filter(visit_detail = visit)
      #for c in vc:
        #visit_soap_objs.append(c)

    visit_soap_objs = VisitSOAP.objects.filter(visit_detail = visit_detail_obj)
    data = []

    if visit_soap_objs:
        for soap in visit_soap_objs:
            if not getattr(soap, 'urls', None):
              soap.save()
            i = 0
            data_to_append = {}
            data_to_append['id'] = soap.id
            data_to_append['objective'] = soap.objective
            data_to_append['subjective'] = soap.subjective
            data_to_append['assessment'] = soap.assessment
            data_to_append['plan'] = soap.plan
            data_to_append['edit'] = soap.urls['edit']
            data_to_append['del'] = soap.urls['del']
            data.append(data_to_append)
            i += 1

    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type="application/json")



@login_required
def visit_soap_add(request, visit_id = None):

    """ 
    Adds a Visit soap
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

        visit_soap_objs = VisitSOAP.objects.filter(visit_detail = visit_detail_obj)
        if visit_soap_objs:
          return visit_soap_edit(request, visit_soap_id = visit_soap_objs[0].id)

        visit_soap_obj = VisitSOAP(visit_detail=visit_detail_obj)

        if request.method == "GET" and request.is_ajax():

            visit_soap_form = VisitSOAPForm(instance = visit_soap_obj,
                                                      auto_id  = "id_add_visit_soap"+ str(visit_id)+"_%s")
            variable = RequestContext(request, {
                                                'user': user,
                                                'visit_detail_obj': visit_detail_obj,
                                                'visit_soap_form': visit_soap_form,
                                                'patient_detail_obj': patient_detail_obj,
                                                'error_message': error_message,
                                                'success': success,
                                                'visit_soap_action':'add'
                                            })

            return render_to_response('visit_soap/add_or_edit_form.html', variable)

        elif request.method == "POST" and request.is_ajax():

            visit_soap_form = VisitSOAPForm(request.POST, instance = visit_soap_obj)

            if visit_soap_form.is_valid() :
                saved_visit_soap = visit_soap_form.save(commit=False)
                saved_visit_soap.visit_detail = visit_detail_obj
                saved_visit_soap.save()
                success = True
                error_message = "History Added Successfully"
                redirectUrl = saved_visit_soap.urls['edit']

            else:
                error_message = ''' <h4>
                                      History Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_soap_form)
                error_message += ('\n' + errors)
                redirectUrl = None
                success = False

            data = {'success': success,
                    'error_message': error_message,
                    'redirectUrl': redirectUrl
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")


@login_required
def visit_soap_edit(request, visit_soap_id = None):

    user = request.user
    error_message = None    
    
    try:

        if visit_soap_id:
          visit_soap_id = int(visit_soap_id)

        else:
          visit_soap_id = int(request.GET.get('visit_soap_id'))

        visit_soap_obj = VisitSOAP.objects.get(pk=visit_soap_id)
        visit_detail_obj = visit_soap_obj.visit_detail
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        if not getattr(patient_detail_obj,'urls',None):
          patient_detail_obj.save()

        if not getattr(visit_soap_obj,'urls',None):
          visit_soap_obj.save()

        if request.method == "GET" and request.is_ajax():

            visit_soap_form = VisitSOAPForm(instance = visit_soap_obj,
                                            auto_id = "id_edit_visit_soap"+    str(visit_soap_id)+"_%s"
                                            )

            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_soap_obj': visit_soap_obj,
                          'visit_soap_form'  : visit_soap_form  ,
                          'patient_detail_obj': visit_detail_obj.patient_detail,
                          'error_message': error_message,
                          'visit_soap_action':'edit'
                          })

            return render_to_response('visit_soap/add_or_edit_form.html', variable)

        if request.method == "POST" and request.is_ajax():

            visit_soap_form   = VisitSOAPForm(request.POST, instance = visit_soap_obj)

            if visit_soap_form.is_valid()    :

                saved_visit_soap = visit_soap_form.save(commit=False)
                saved_visit_soap.visit_detail = visit_detail_obj
                saved_visit_soap.save()
                success = True
                error_message = "Visit SOAP Edited Successfully"
                redirectUrl = saved_visit_soap.urls['edit']

            else:
                success = False
                error_message = ''' <h4>
                                      Visit SOAP Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_soap_form)
                error_message += ('\n' + errors)
                redirectUrl = None

            data = {'success': success, 'error_message': error_message , 'redirectUrl': redirectUrl }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        else:
             raise Http404(" Error ! Unsupported Request..")


    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitSOAP.DoesNotExist):
        raise Http404("Requested VisitSOAP Does not exist.")


@login_required
def visit_soap_del(request, visit_soap_id = None):
    
    if request.method == "GET" and request.is_ajax():

        user = request.user

        try:
            if visit_soap_id:
              visit_soap_id = int(visit_soap_id)
            else:
              visit_soap_id = int(request.GET.get('visit_soap_id'))

            visit_soap_obj = VisitSOAP.objects.get(pk=visit_soap_id)
            visit_detail_obj = visit_soap_obj.visit_detail

            if not getattr(visit_detail_obj,'urls', None):
              visit_detail_obj.save()

            visit_soap_obj.delete()
            error_message = None
            success = True
            error_message = "Successfully Deleted Visit SOAP "
            data = {'success': success, 
                    'error_message': error_message, 
                    'redirectUrl': visit_detail_obj.urls['add']['visit_soap'] 
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitSOAP.DoesNotExist):
            raise Http404("Requested Visit SOAP Does not exist.")

    else:
        raise Http404(" Error ! Unsupported Request..")