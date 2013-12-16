#################################################################################
# Project     : AuShadha
# Description : AuShadha Views for OPD Visits
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
#import ho.pisa                      as pisa
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
#from AuShadha.apps.clinic.models import Clinic
from registry.inv_and_imaging.models import LabInvestigationRegistry, ImagingInvestigationRegistry

PatientDetail = UI.get_module('PatientRegistration')
AdmissionDetail = UI.get_module('Admission')
#from patient.models import PatientDetail
#from admission.models import AdmissionDetail

from .models import VisitDetail, VisitDetailForm
from dijit_widgets.tree import VisitTree



# views start here;;
@login_required
def visit_list(request):
    if request.user:
        user = request.user
        if request.method == "GET":
            visit_obj = VisitDetail.objects.all().order_by('visit_date')
            variable = RequestContext(request, {'user': user,
                                                'visit_obj': visit_obj,
                                                })
            return render_to_response('visit_detail/visit_list.html', variable)
        else:
            raise Http404("Bad Request:: " + str(request.method) + " ")
    else:
        return HttpResponseRedirect('/AuShadha/login/')




@login_required
def visit_json(request, patient_id = None):
    try:
        action = unicode(request.GET.get('action'))
        if patient_id:
          patient_id = int(patient_id)
        else:
          patient_id = int(request.GET.get('patient_id'))          
        if action == 'add':
            return patient_visit_add(request, patient_id)
        patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")
    patient_visit_obj = VisitDetail.objects.filter(
        patient_detail=patient_detail_obj)
    data = []
    if patient_visit_obj:
        for visit in patient_visit_obj:
            i = 0
            data_to_append = {}
            data_to_append['id'] = visit.id
            data_to_append[
                'visit_date'] = visit.visit_date.date().isoformat() + i
            data_to_append['op_surgeon'] = visit.op_surgeon.__unicode__()
            data_to_append['is_active'] = visit.is_active
            data_to_append['referring_doctor'] = visit.referring_doctor
            data_to_append['consult_nature'] = visit.consult_nature
            data_to_append['remarks'] = visit.remarks
            data_to_append['edit'] = visit.get_edit_url()
            data_to_append['del'] = visit.get_del_url()
            data.append(data_to_append)
            i += 1
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")


@login_required
def visit_summary(request, patient_id = None):
  pass


@login_required
def render_visit_json(request):

    if request.method =='GET':
      all_v = VisitDetail.objects.all()
      if all_v is not None:
          data = []
          for visit in all_v:
              print "Evaluating Visit.. "
              print visit
              json = ModelInstanceJson(visit).return_data()
              data.append(json)
      else:
        data = {}
      json = simplejson.dumps(data)
      print "\n"
      print "-" *100
      print "Printing Sample Visit JSON"
      print "-" *100
      print (simplejson.dumps(data[0]))
      print "-" *100
      print "\n"
      return HttpResponse(json, content_type="application/json")
    else:
      raise Http404("Bad Request Method")



@login_required
def render_visit_tree(request,patient_id = None):

  if request.method == "GET" and request.is_ajax():

    if patient_id:
      patient_id = int( patient_id )

    else:
      try:
        patient_id = int( request.GET.get('patient_id') )
      except (KeyError, NameError, ValueError,AttributeError):
        raise Http404("Bad Request: Invalid Request Parameters")

    try:
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")      

    d = {'request' : request,
         'patient': patient_detail_obj,
         'can_add_new_visit' : patient_detail_obj.can_add_new_visit(patient_detail_obj),
         'active_visits' : VisitDetail.objects.filter(patient_detail = patient_detail_obj).filter(is_active = True),
         'all_visits' : VisitDetail.objects.filter(patient_detail = patient_detail_obj),
         'inactive_visits': VisitDetail.objects.filter(patient_detail = patient_detail_obj).filter(is_active = False)
         }

    tree = VisitTree(d)()
    return HttpResponse(tree, content_type="application/json")

  else:
      raise Http404("Bad Request")




@login_required
def render_visit_list(request):
    """View for Generating Visit List Takes on Request Object as argument."""
    user = request.user
    keys = [
        "sort( date_of_visit)", "sort(-date_of_visit)", "sort(+date_of_visit)",
        "sort( op_surgeon)", "sort(-op_surgeon)", "sort(+op_surgeon)",
    ]
    key_sort_map = {
        "sort(+date_of_visit)": "visit_date",
        "sort( date_of_visit)": "visit_date",
        "sort(-date_of_visit)": "-visit_date",
        "sort(+op_surgeon)": "op_surgeon",
        "sort( op_surgeon)": "op_surgeon",
        "sort(-op_surgeon)": "-op_surgeon",
    }
    for key in request.GET:
        if key in keys:
            sort = key_sort_map[key]
            all_visits = VisitDetail.objects.all().order_by(sort)
        else:
            all_visits = VisitDetail.objects.all().order_by('-visit_date')
    data = []
    for visit in all_visits:
        data_to_append = {}
        data_to_append['id'] = visit.id
        data_to_append['date_of_visit'] = visit.visit_date.strftime(
            "%d/%m/%Y %H:%M:%S")
        data_to_append['surgeon'] = visit.op_surgeon.__unicode__()
        data_to_append[
            'patient_hospital_id'] = visit.patient_detail.patient_hospital_id
        data_to_append['patient'] = visit.patient_detail.__unicode__()
        data_to_append['age'] = visit.patient_detail.age
        data_to_append['sex'] = visit.patient_detail.sex
        data_to_append['active'] = visit.is_active
        data_to_append['del'] = visit.get_edit_url()
        data_to_append['edit'] = visit.get_del_url()
        data.append(data_to_append)
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")



@login_required
def visit_detail_list(request, patient_id = None):
    user = request.user

    if request.method == "GET" and request.is_ajax():
        try:

            if patient_id:
              patient_id = int(patient_id)

            else:
              patient_id = int(request.GET.get('patient_id'))

            patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
            visit_detail_obj = VisitDetail.objects.filter(patient_detail=patient_detail_obj).order_by('-visit_date')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (PatientDetail.DoesNotExist):
            raise Http404("Requested Patient Does not exist.")

        visit_form_list = []

        if visit_detail_obj:
            error_message = None
            for visit in visit_detail_obj:
                visit_form_list.append([VisitDetailForm(instance=visit), visit])

        else:
            error_message = "No Visits Recorded"

        variable = RequestContext(request, {'user': user,
                                            'visit_detail_obj': visit_detail_obj,
                                            'visit_form_list': visit_form_list,
                                            'patient_detail_obj': patient_detail_obj,
                                            'error_message': error_message
                                            })
        return render_to_response('visit_detail/list.html', variable)

    else:
        raise Http404(" Error ! Unsupported Request..")



@login_required
def visit_detail_add(request, patient_id = None, nature='initial'):

    """ 
        Adds a new VisitDetail Object
        Takes request and id of PatientDetail object
        the nature of visit is defaulted to 'initial'.
        Implementation of separate visits for 'initial' , 'fu' etc.. can be implemented later.
    """
    print "Received request to add VisitDetail"

    user = request.user
    success = False
    error_message = None
    form_errors = []

    try:
        if patient_id:
          patient_id = int(patient_id)
        else:
          patient_id = int(request.GET.get('patient_id'))

        patient_detail_obj = PatientDetail.objects.get(pk=patient_id)

        if not getattr(patient_detail_obj, 'urls', None):
          patient_detail_obj.save()

        if not patient_detail_obj.can_add_new_visit(patient_detail_obj):
            error_message = '''
                              Cannot add new visit now.
                              There may be a active admission / visit. 
                              Please close that and try again
                            '''
            raise Http404(error_message)

        else:
            print patient_detail_obj, " can add VisitDetail"
            visit_detail_obj = VisitDetail(patient_detail=patient_detail_obj)

            if request.method == "GET" and request.is_ajax():

                if nature == 'initial':
                    visit_detail_form = VisitDetailForm(initial={'visit_date': datetime.now().date().isoformat(),
                                                                'consult_nature': 'initial',
                                                                'status': 'examining',
                                                                'op_surgeon': user
                                                                },
                                                        instance = visit_detail_obj,
                                                        auto_id = "id_new_visit_detail" + str(id) + "_%s")

                    if not getattr(patient_detail_obj, 'urls' , None):
                      patient_detail_obj.save()

                    variable = RequestContext(
                        request, {
                            'user': user,
                            'visit_detail_obj': visit_detail_obj,
                            'visit_detail_form': visit_detail_form,
                            'patient_detail_obj': patient_detail_obj,
                            'error_message': error_message,
                            'success': success,
                            'form_action':'add'
                        })
                    return render_to_response('visit_detail/add.html', variable)

                elif nature == 'fu':
                    # TODO
                    pass

            elif request.method == "POST" and request.is_ajax():
                print "Received request to add visit..."
                visit_detail_form = VisitDetailForm(request.POST, instance=visit_detail_obj)

                if visit_detail_form.is_valid():
                    saved_visit = visit_detail_form.save()
                    success = True
                    error_message = "Visit Added Successfully"

                else:
                    error_message = ''' <h4>Visit Could not be Saved.
                                        Please check the forms for errors
                                        </h4>
                                    '''
                    errors = aumodelformerrorformatter_factory(visit_detail_form) + '\n'

                data = {'success': success,
                        'error_message': error_message
                        }
                json = simplejson.dumps(data)
                return HttpResponse(json, content_type='application/json')

            else:
                raise Http404(" Error ! Unsupported Request..")

    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (PatientDetail.DoesNotExist):
        raise Http404("Requested Patient Does not exist.")



@login_required
def visit_detail_edit(request, visit_id = None):

    user = request.user
    error_message = None    
    success = False

    try:
        if visit_id:
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        form_field_auto_id = 'id_edit_visit_detail_' + str(visit_id)
        data = {'visit_date': visit_detail_obj.visit_date.date().isoformat()}

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        if request.method == "GET" and request.is_ajax():

            visit_detail_form = VisitDetailForm(initial=data, 
                                                instance=visit_detail_obj, 
                                                auto_id=form_field_auto_id + "_%s"
                                                )

            variable = RequestContext(request, 
                                      {'user': user,
                                        'visit_detail_obj': visit_detail_obj,
                                        'visit_detail_form': visit_detail_form,
                                        'patient_detail_obj': visit_detail_obj.patient_detail,
                                        'error_message': error_message,
                                        'form_action':'edit'
                                      })
            return render_to_response('visit_detail/edit.html', variable)

        elif request.method == "POST" and request.is_ajax():

            visit_detail_form = VisitDetailForm(request.POST, instance=visit_detail_obj)

            if visit_detail_form.is_valid():
                saved_visit = visit_detail_form.save()
                success = True
                error_message = "Visit Edited Successfully"

            else:
                error_message = ''' <h4>
                                        Visit Could not be Saved.
                                        Please check the forms for errors
                                    </h4>
                                '''
                errors = aumodelformerrorformatter_factory(visit_detail_form)     + '\n'
                error_message += ('\n' + errors)

            data = {'success': success,
                    'error_message': error_message
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")          

    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")

    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Patient Does not exist.")    



@login_required
def visit_detail_del(request, visit_id = None):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        try:
            if visit_id:
              visit_id = int(visit_id)
            else:
              visit_id = int(request.GET.get('visit_id'))
            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            error_message = None
            visit_detail_obj.delete()
            success = True
            error_message = "Successfully Deleted Visit."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Patient Does not exist.")

    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_close(request, visit_id = None):

    if request.method == "GET" and request.is_ajax():
        user = request.user

        try:
            if visit_id :
              visit_id= int(visit_id)
            else:
              visit_id = int(request.GET.get('visit_id'))

            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            # visit_detail_obj._close_all_active_visits()
            visit_detail_obj._close_visit()
            error_message = None
            success = True
            error_message = "Successfully Closed Visit."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")

    else:
        raise Http404(" Error ! Unsupported Request..")
