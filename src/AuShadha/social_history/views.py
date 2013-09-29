#####################################################################################
# PROJECT      : AuShadha
# Description  : Social History Views
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#####################################################################################



# General Module imports-----------------------------------
from datetime import datetime, date, time

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core.paginator import Paginator
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder
#from django.template.response import TemplateResponse
#from django.contrib.sites.models import get_current_site
#import urlparse

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid

from patient.models import PatientDetail
from social_history.models import SocialHistory, SocialHistoryForm


# Views start here -----------------------------------------

@login_required
def social_history_json(request, patient_id = None):
    try:
        
        if patient_id:
          patient_id = int(patient_id)
        else:
          patient_id = int(request.GET.get('patient_id'))
          action = unicode(request.GET.get('action'))          

        if action == 'add':
            return social_history_add(request, patient_id)

        patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
        social_history_obj = SocialHistory.objects.filter(patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(social_history_obj)
        return HttpResponse(json, content_type="application/json")
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
      raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")


@login_required
def social_history_add(request, patient_id = None):

    if request.user:
        user = request.user
        try:
          if patient_id:
            patient_id = int(patient_id)
          else:
            patient_id = int(request.GET.get('patient_id'))

          patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
          patient_detail_obj.generate_urls()
          social_history_obj = SocialHistory.objects.filter(patient_detail=patient_detail_obj)

          if social_history_obj:
              return social_history_edit(request, social_history_obj[0].id)
          else:
              social_history_obj = SocialHistory(patient_detail=patient_detail_obj)

          if request.method == "GET" and request.is_ajax():
                social_history_form = SocialHistoryForm(instance=social_history_obj)

                variable = RequestContext(request,
                                          {"user": user,
                                            "patient_detail_obj": patient_detail_obj,
                                            "social_history_form": social_history_form,
                                            "social_history_obj": social_history_obj,
                                            'button_label': "Add",
                                            "action": patient_detail_obj.urls['add']['social_history'],
                                            "addUrl": patient_detail_obj.urls['add']['social_history'],
                                            'canDel': False,
                                            'editUrl': None,
                                            'delUrl': None
                                            })
                return render_to_response('social_history/add_or_edit_form.html', variable)

          elif request.method == 'POST' and request.is_ajax():
                  copy_post = request.POST.copy()

                  #print "Received POST Request with", request.POST
                  #print "Home Occupants received are", copy_post.getlist('home_occupants')

                  copy_post['home_occupants'] = ",".join(copy_post.getlist('home_occupants'))
                  copy_post['pets'] = ",".join(copy_post.getlist('pets'))
                  
                  social_history_form = SocialHistoryForm(copy_post, instance=social_history_obj)

                  if social_history_form.is_valid():
                      try:
                          social_history_obj = social_history_form.save()
                          success = True
                          error_message = "SocialHistory Data Added Successfully"
                          form_errors = None
                          addData = {
                              "marital_status": social_history_obj.marital_status,
                              "marital_status_notes": social_history_obj.marital_status_notes,
                              "occupation": social_history_obj.occupation,
                              "occupation_notes": social_history_obj.occupation_notes,
                              "exercise": social_history_obj.exercise,
                              "exercise_notes": social_history_obj.exercise_notes,
                              "diet": social_history_obj.diet,
                              "diet_notes": social_history_obj.diet_notes,
                              "home_occupants": social_history_obj.home_occupants,
                              "home_occupants_notes": social_history_obj.home_occupants_notes,
                              "pets": social_history_obj.pets,
                              "pets_notes": social_history_obj.pets_notes,
                              "alcohol": social_history_obj.alcohol,
                              "alcohol_no": social_history_obj.alcohol_no,
                              "alcohol_notes": social_history_obj.alcohol_notes,
                              "tobacco": social_history_obj.tobacco,
                              "tobacco_no": social_history_obj.tobacco_no,
                              "tobacco_notes": social_history_obj.tobacco_notes,
                              "drug_abuse": social_history_obj.drug_abuse,
                              "drug_abuse_notes": social_history_obj.drug_abuse_notes,
                              "sexual_preference": social_history_obj.sexual_preference,
                              "sexual_preference_notes": social_history_obj.sexual_preference_notes,
                              "current_events": social_history_obj.current_events
                          }
                          data = {'success': success,
                                  'error_message': error_message,
                                  'form_errors': form_errors,
                                  'canDel': True,
                                  'addUrl': None,
                                  "addData": addData,
                                  'editUrl': social_history_obj.urls['edit'],
                                  'delUrl': social_history_obj.urls['del'],
                                  }
                      except (Exception("SocialHistoryExistsError")):
                          data = {'success': False,
                                  'error_message': "Social History Already Exists ! Cannot add More",
                                  'form_errors': error_message,
                                  'addData':None
                                  }
                  else:
                      data = {'success': False,
                              'error_message': aumodelformerrorformatter_factory(social_history_form),
                              'form_errors': error_message,
                              'addData':None
                              }
                  json = simplejson.dumps(data)
                  return HttpResponse(json, content_type='application/json')

          else:
              raise Http404(
                  "BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))

        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")

        except (PatientDetail.DoesNotExist):
            raise Http404("BadRequest: Patient Data Does Not Exist")



@login_required
def social_history_edit(request, social_history_id = None):

    if request.user:
        user = request.user

        try:
          if social_history_id:
            social_history_id = int(social_history_id)
          else:
            social_history_id = int(request.GET.get('social_history_id'))
          social_history_obj = SocialHistory.objects.get(pk=social_history_id)

        except ValueError or AttributeError or TypeError:
            raise Http404("BadRequest: Server Error")
        except SocialHistory.DoesNotExist:
            raise Http404("BadRequest: Requested Patient SocialHistory Data DoesNotExist")

        if request.method == "GET" and request.is_ajax():
                social_history_form = SocialHistoryForm(instance=social_history_obj)
                patient_detail_obj = social_history_obj.patient_detail
                addData = {
                    "marital_status": social_history_obj.marital_status,
                    "marital_status_notes": social_history_obj.marital_status_notes,
                    "occupation": social_history_obj.occupation,
                    "occupation_notes": social_history_obj.occupation_notes,
                    "exercise": social_history_obj.exercise,
                    "exercise_notes": social_history_obj.exercise_notes,
                    "diet": social_history_obj.diet,
                    "diet_notes": social_history_obj.diet_notes,
                    "home_occupants": social_history_obj.home_occupants,
                    "home_occupants_notes": social_history_obj.home_occupants_notes,
                    "pets": social_history_obj.pets,
                    "pets_notes": social_history_obj.pets_notes,
                    "alcohol": social_history_obj.alcohol,
                    "alcohol_no": social_history_obj.alcohol_no,
                    "alcohol_notes": social_history_obj.alcohol_notes,
                    "tobacco": social_history_obj.tobacco,
                    "tobacco_no": social_history_obj.tobacco_no,
                    "tobacco_notes": social_history_obj.tobacco_notes,
                    "drug_abuse": social_history_obj.drug_abuse,
                    "drug_abuse_notes": social_history_obj.drug_abuse_notes,
                    "sexual_preference": social_history_obj.sexual_preference,
                    "sexual_preference_notes": social_history_obj.sexual_preference_notes,
                    "current_events": social_history_obj.current_events
                }
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "social_history_form": social_history_form,
                                           "social_history_obj": social_history_obj,
                                           "addData": addData,
                                           'action': social_history_obj.urls['edit'],
                                           'button_label': "Edit",
                                           'canDel': True,
                                           'addUrl': None,
                                           'editUrl': social_history_obj.urls['edit'],
                                           'delUrl': social_history_obj.urls['del'],
                                           })
                return render_to_response('social_history/add_or_edit_form.html', variable)

        elif request.method == 'POST' and request.is_ajax():
                copy_post = request.POST.copy()
                copy_post['home_occupants'] = ",".join(copy_post.getlist('home_occupants'))
                copy_post['pets'] = ",".join(copy_post.getlist('pets'))
                social_history_form = SocialHistoryForm(copy_post, instance=social_history_obj)
                patient_detail_obj = social_history_obj.patient_detail

                if social_history_form.is_valid():
                    social_history_obj = social_history_form.save()
                    success = True
                    error_message = "SocialHistory Data Edited Successfully"
                    form_errors = ''
                    addData = {
                        "marital_status": social_history_obj.marital_status,
                        "marital_status_notes": social_history_obj.marital_status_notes,
                        "occupation": social_history_obj.occupation,
                        "occupation_notes": social_history_obj.occupation_notes,
                        "exercise": social_history_obj.exercise,
                        "exercise_notes": social_history_obj.exercise_notes,
                        "diet": social_history_obj.diet_notes,
                        "home_occupants": social_history_obj.home_occupants,
                        "home_occupants_notes": social_history_obj.home_occupants_notes,
                        "pets": social_history_obj.pets,
                        "pets_notes": social_history_obj.pets_notes,
                        "alcohol": social_history_obj.alcohol,
                        "alcohol_no": social_history_obj.alcohol_no,
                        "alcohol_notes": social_history_obj.alcohol_notes,
                        "tobacco": social_history_obj.tobacco,
                        "tobacco_no": social_history_obj.tobacco_no,
                        "tobacco_notes": social_history_obj.tobacco_notes,
                        "drug_abuse": social_history_obj.drug_abuse,
                        "drug_abuse_notes": social_history_obj.drug_abuse_notes,
                        "sexual_preference": social_history_obj.sexual_preference,
                        "sexual_preference_notes": social_history_obj.sexual_preference_notes,
                        "current_events": social_history_obj.current_events
                    }
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors,
                            "addData": addData
                            }
                else:
                    data = {'success': False, 
                            'error_message': aumodelformerrorformatter_factory(social_history_form), 
                            'form_errors':error_message,
                            'addData':None
                            }
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def social_history_del(request, social_history_id):
    user = request.user
    if user and user.is_superuser:
        if request.method == "GET":
            try:
              if social_history_id:
                social_history_id = int(social_history_id)
              else:
                social_history_id = int(request.GET.get('social_history_id'))
              social_history_obj = SocialHistory.objects.get(pk=social_history_id)
              patient_detail_obj  = social_history_obj.patient_detail
              patient_detail_obj.generate_urls()
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except SocialHistory.DoesNotExist:
                raise Http404("BadRequest: SocialHistory Data Does Not Exist")

            social_history_obj.delete()
            success = True
            error_message = "SocialHistory Data Deleted Successfully"
            data = {'success': success,
                    'error_message': error_message,
                    'addUrl': patient_detail_obj.urls['add']['social_history'],
                    'canDel': False,
                    'editUrl': None,
                    'delUrl': None
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")