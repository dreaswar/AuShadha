################################################################################
# Project     : AuShadha
# Description : Views for / visit_prescription
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 16-09-2013
################################################################################


# General Module imports-----------------------------------
from datetime import datetime, date, time

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

import json
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.clinic.models import Clinic
from AuShadha.apps.ui.ui import ui as UI

from .models import VisitPrescription, VisitPrescriptionForm 
from dijit_widgets.tree import VisitPrescriptionTree

VisitDetail = UI.get_module('OPD_Visit')


# Views start here -----------------------------------------


@login_required
def visit_prescription_list(request, visit_detail_id = None):
   """ lists the prescriptions for a visit """
   print("Listing Visit Prescriptions")
   try:
        if visit_detail_id: 
            visit_detail_id = int(visit_detail_id)
        else:
            try:
                visit_detail_id = int( request.GET.get('visit_detail_id') )
            except(TypeError,KeyError,NameError,ValueError):
                raise Http404("Bad Request Parameter.")
        visit_detail_obj = VisitDetail.objects.get(pk=visit_detail_id)
        visit_prescription_objs = VisitPrescription.objects.filter(visit_detail = visit_detail_obj)
        jsondata = []
        for prescription in visit_prescription_objs:
            jsondata.append(ModelInstanceJson(prescription).return_data())
        data = json.dumps(jsondata)
        print("Prescriptions requested are: ")
        print(data)
        return HttpResponse(data, content_type='application/json')

   except(ValueError,NameError,KeyError,TypeError):
       raise Http404("Bad Request Parameters")
   except(VisitDetail.DoesNotExist):
       raise Http404("Invalid Visit Request.No Visit with the ID specified exists")
   
@login_required
def visit_prescription_json(request,visit_detail_id=None):
    return visit_prescription_list(request,visit_detail_id)

@login_required
def visit_prescription_add(request,visit_detail_id = None):
    """ 
    Adds a Visit prescription
    """

    user = request.user
    success = False
    error_message = None
    form_errors = []

    try:
        if visit_detail_id:
          visit_detail_id = int(visit_detail_id)
        else:
          visit_detail_id = int(request.GET.get('visit_detail_id'))

        visit_detail_obj = VisitDetail.objects.get(pk=visit_detail_id)
        patient_detail_obj = visit_detail_obj.patient_detail
        visit_prescription_obj = VisitPrescription(visit_detail=visit_detail_obj)

        if not getattr(patient_detail_obj, 'urls', None):
          patient_detail_obj.save()

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()

        if request.method == "GET" and request.is_ajax():

            visit_prescription_form = VisitPrescriptionForm(instance = visit_prescription_obj,
                                                      auto_id  =
                                                      "id_add_visit_prescription"+
                                                      str(visit_detail_id)+"_%s")
            variable = RequestContext(request, {
                                                'user': user,
                                                'visit_detail_obj': visit_detail_obj,
                                                'form': visit_prescription_form,
                                                'patient_detail_obj': patient_detail_obj,
                                                'error_message': error_message,
                                                'success': success,
                                            })

            return render_to_response('visit_prescription/forms/add.html', variable)

        elif request.method == "POST" and request.is_ajax():

            visit_prescription_form = VisitPrescriptionForm(request.POST, instance = visit_prescription_obj)

            if visit_prescription_form.is_valid() :
                saved_visit_prescription = visit_prescription_form.save(commit=False)
                saved_visit_prescription.visit_detail = visit_detail_obj
                #TODO: Custom date-range handling
                #TODO: Custom admin hours handling
                saved_visit_prescription.save()
                success = True
                error_message = "Prescription Added Successfully"

            else:
                error_message = ''' <h4>
                                      Prescription could not be saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_prescription_form)
                error_message += ('\n' + errors)

            data = {'success': success,
                    'error_message': error_message
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
def visit_prescription_edit(request, visit_prescription_id):
  
    user = request.user
    error_message = None    
    try:
        if visit_prescription_id:
          visit_prescription_id = int(visit_prescription_id)
        else:
          visit_prescription_id = int(request.GET.get('visit_prescription_id'))
        visit_prescription_obj = VisitPrescription.objects.get(pk=visit_prescription_id)
        visit_detail_obj = visit_prescription_obj.visit_detail
        patient_detail_obj = visit_detail_obj.patient_detail

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        if not getattr(patient_detail_obj,'urls',None):
          patient_detail_obj.save()

        if not getattr(visit_prescription_obj,'urls',None):
          visit_prescription_obj.save()
        
        if request.method == "GET" and request.is_ajax():
            visit_prescription_form = VisitPrescriptionForm(instance = visit_prescription_obj, 
                                                          auto_id = False
                                                        )
            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_prescription_obj': visit_prescription_obj,
                          'form'  : visit_prescription_form  ,
                          'patient_detail_obj': visit_detail_obj.patient_detail,
                          'error_message': error_message,
                          'form_action':'edit'
                          })
            return render_to_response('visit_prescription/forms/edit.html', variable)

        if request.method == "POST" and request.is_ajax():
            visit_prescription_form   = VisitPrescriptionForm(request.POST, instance = visit_prescription_obj )
            if visit_prescription_form.is_valid():
                saved_visit_prescription = visit_prescription_form.save(commit=False)
                saved_visit_prescription.visit_detail = visit_detail_obj
                saved_visit_prescription.save()
                success = True
                error_message = "Visit Edited Successfully"
                #if check_duplicates(saved_visit_prescription, visit_detail_obj):
                    #saved_visit_prescription.save()
                    #success = True
                    #error_message = "Visit Edited Successfully"
                #else:
                    #success = False
                    #error_message = ''' <h4>
                                        #Visit Could not be Saved as there are duplicate prescription.
                                        #Please check the forms for errors
                                        #</h4>
                                    #'''
            else:
                success = False
                error_message = ''' <h4>
                                      Visit Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                errors += aumodelformerrorformatter_factory(visit_prescription_form)
                error_message += ('\n' + errors)
            data = {'success': success, 'error_message': error_message }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')
        else:
             raise Http404(" Error ! Unsupported Request..")
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitPrescription.DoesNotExist):
        raise Http404("Requested VisitPrescription Does not exist.")


@login_required
def visit_prescription_del(request, visit_prescription_id):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        try:
            if visit_prescription_id:
              visit_prescription_id = int(visit_prescription_id)
            else:
              visit_prescription_id = int(request.GET.get('visit_prescription_id'))
            visit_prescription_obj = VisitPrescription.objects.get(pk=visit_prescription_id)
            error_message = None
            visit_prescription_obj.delete()
            success = True
            error_message = "Successfully Deleted Visit Prescription "
            data = {'success': success, 'error_message': error_message}
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')
        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitPrescription.DoesNotExist):
            raise Http404("Requested Visit Prescription Does not exist.")
    else:
        raise Http404(" Error ! Unsupported Request..")


def return_visit_prescription_json( instance ,success = True):
   json_obj = ModelInstanceJson(instance)
   return json_obj()

@login_required
def render_visit_prescription_tree(request,visit_detail_id = None):
  pass

@login_required
def render_visit_prescription_summary(request, visit_detail_id=None):
  pass

@login_required
def render_visit_prescription_json(request, id = None):
  pass
