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

from .models import VisitComplaint, VisitComplaintAddForm, VisitComplaintEditForm


# Module Vars:
complaint_add_icon_template = get_template(
    'visit_template_snippets/icons/complaints_add.html')
complaint_remove_icon_template = get_template(
    'visit_template_snippets/icons/complaints_remove.html')

generic_table_form_add_icon_template = get_template(
    'visit_template_snippets/icons/generic_add_icon.html')
generic_table_form_remove_icon_template = get_template(
    'visit_template_snippets/icons/generic_remove_icon.html')


# views start here;;


@login_required
def visit_complaint_add(request, visit_id = None):

    """ 
    Adds a Visit complaint
    """

    user = request.user
    success = False
    error_message = None
    form_errors = []

    visit_complaint_formset_prefix="visit_complaints"

    generic_add_icon_html = generic_table_form_add_icon_template.render(RequestContext(request, {'user': user}))
    generic_remove_icon_html = generic_table_form_remove_icon_template.render(RequestContext(request, {'user': user}))
    complaint_add_icon_html = complaint_add_icon_template.render(RequestContext(request, {'user': user}))
    complaint_remove_icon_html = complaint_remove_icon_template.render(RequestContext(request, {'user': user}))

    complaint_form_var_dict = {'prefix': visit_complaint_formset_prefix,
                                'total_form_id': visit_complaint_formset_prefix+"-TOTAL_FORMS",
                                'form_count':''
                                } 

    try:
        if visit_id:
          visit_id = int(patient_id)
        else:
          visit_id = int(request.GET.get('visit_id'))

        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail
        visit_complaint_obj = VisitComplaint(visit_detail=visit_detail_obj)

        if not getattr(visit_detail_obj, 'urls', None):
          visit_detail_obj.save()

        if not getattr(patient_detail_obj, 'urls', None):
          patient_detail_obj.save()

        VisitComplaintFormset = modelformset_factory(VisitComplaint,
                                                     form=VisitComplaintAddForm,
                                                     can_delete=True,
                                                     can_order=True,
                                                    )

        complaint_form_auto_id = "id_"+ visit_complaint_formset_prefix + "_new_complaint_" + str(visit_id)
        complaint_total_form_auto_id = "id_"+visit_complaint_formset_prefix + "-TOTAL_FORMS_new_complaint_" + str(visit_id)

        if request.method == "GET" and request.is_ajax():

            visit_complaint_formset = VisitComplaintFormset(queryset=VisitComplaint.objects.none(),
                                                            auto_id=complaint_form_auto_id,
                                                            prefix=visit_complaint_formset_prefix
                                                            )

            #complaint_formset_auto_id = "id_%s"+"_add_visit_complaint_"+ str(id)
            #complaint_total_form_auto_id = "id_form-TOTAL_FORMS_add_visit_complaint_"+str(id)

            # visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj,
                                                      # auto_id  =
                                                      # "id_new_visit_complaint"+
                                                      # str(id)+"_%s")
            variable = RequestContext(request, {
                                                'user': user,
                                                'visit_detail_obj': visit_detail_obj,
                                                'visit_complaint_formset': visit_complaint_formset,
                                                #'visit_complaint_form_html'   : visit_complaint_form_html,
                                                'patient_detail_obj': patient_detail_obj,
                                                'error_message': error_message,
                                                'complaint_add_icon_html': complaint_add_icon_html,
                                                'complaint_remove_icon_html': complaint_remove_icon_html,
                                                'generic_add_icon_html':generic_add_icon_html,
                                                'generic_remove_icon_html':generic_remove_icon_html,
                                                'success': success,
                                                'complaint_form_auto_id': complaint_form_auto_id,
                                                'complaint_total_form_auto_id': visit_complaint_formset_prefix+"-TOTAL_FORMS",
                                                'form_action':'add'
                                            })
            
            return render_to_response('visit_complaint/add.html', variable)

        elif request.method == "POST" and request.is_ajax():

            #visit_complaint_form = VisitComplaintForm(request.POST, instance = visit_complaint_obj)
            #VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)
            visit_complaint_formset = VisitComplaintFormset(request.POST, 
                                                            auto_id=complaint_form_auto_id,
                                                            prefix=visit_complaint_formset_prefix
                                                            )

            if visit_complaint_formset.is_valid() :
                saved_visit_complaints = visit_complaint_formset.save(commit=False)
                for complaint in saved_visit_complaints:
                    complaint.visit_detail = visit_detail_obj
                    complaint.save()
                success = True
                error_message = "Visit Added Successfully"

            else:
                error_message = ''' <h4>
                                      Visit Could not be Saved.
                                      Please check the forms for errors
                                    </h4>
                                '''
                for form in visit_complaint_formset:
                    errors += aumodelformerrorformatter_factory(form)
                for form in vasc_exam_free_model_formset:
                    errors += aumodelformerrorformatter_factory(form)

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
        raise Http404("Requested Visit Does not exist.")



@login_required
def visit_complaint_edit(request, visit_complaint_id = None):

    user = request.user
    error_message = None    
    VisitComplaintFormset = modelformset_factory(VisitComplaint,
                                                 form=VisitComplaintEditForm,
                                                 extra=0
                                                 )


    if request.method == "GET" and request.is_ajax():

        try:
            if visit_complaint_id:
              visit_complaint_id = int(visit_complaint_id)
            else:
              visit_complaint_id = int(request.GET.get('visit_complaint_id'))

            visit_complaint_obj = VisitComplaint.objects.get(pk=visit_complaint_id)
            visit_detail_obj = visit_complaint_obj.visit_detail

            visit_complaint_formset_prefix="edit_visit_complaints_"+str(visit_complaint_id)
            form_field_auto_id = 'id_edit_visit_detail_' + str(visit_complaint_id)

            complaint_formset_auto_id = "id_"+visit_complaint_formset_prefix +"_edit_visit_complaint_" + str(visit_complaint_id)
            complaint_total_form_auto_id = "id_"+visit_complaint_formset_prefix+"-TOTAL_FORMS_edit_visit_complaint_" + str(visit_complaint_id)

            data = {'visit_date': visit_detail_obj.visit_date.date().isoformat() }

            visit_complaint_formset = VisitComplaintFormset(queryset=VisitComplaint.objects.filter(
                                                                visit_detail=visit_detail_obj),
                                                            auto_id=complaint_formset_auto_id,
                                                            prefix = visit_complaint_formset_prefix
                                                          )


        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")

        except (VisitComplaint.DoesNotExist):
            raise Http404("Requested VisitComplaint Does not exist.")


        complaint_add_icon_template = get_template(
            'visit_template_snippets/icons/complaints_add.html')
        complaint_remove_icon_template = get_template(
                'visit_template_snippets/icons/complaints_remove.html')
        complaint_add_icon_html = complaint_add_icon_template.render(
            RequestContext(request, {'user': user}))
        complaint_remove_icon_html = complaint_remove_icon_template.render(
            RequestContext(request, {'user': user}))

        # if visit_complaint_obj:
            #visit_complaint_obj = visit_complaint_obj[0]
            #c_auto_id = 'id_edit_visit_complaint_'+str(visit_complaint_obj.id)
            #visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj, auto_id = c_auto_id +"_%s")
        # else:
            #visit_complaint_form = None
            #visit_complaint_formset  = None
        generic_add_icon_html = generic_table_form_add_icon_template.render(
            RequestContext(request, {'user': user}))
        generic_remove_icon_html = generic_table_form_remove_icon_template.render(
            RequestContext(request, {'user': user}))

        if not getattr(visit_detail_obj,'urls',None):
          visit_detail_obj.save()

        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      #'visit_complaint_form'  : visit_complaint_form  ,
                      'visit_complaint_formset': visit_complaint_formset,
                      'patient_detail_obj': visit_detail_obj.patient_detail,
                      'error_message': error_message,
                      'complaint_count': complaint_count,
                      'complaint_add_icon_html': complaint_add_icon_html,
                      'complaint_remove_icon_html': complaint_remove_icon_html,
                      'complaint_formset_auto_id': complaint_formset_auto_id,
                      'complaint_total_form_auto_id': visit_complaint_formset_prefix+"-TOTAL_FORMS",
                      'generic_add_icon_html':generic_add_icon_html,
                      'generic_remove_icon_html':generic_remove_icon_html,
                      'form_action':'edit'
                      })
        return render_to_response('visit_complaint/edit.html', variable)

    if request.method == "POST" and request.is_ajax():
        try:
            if visit_id:
              visit_id = int(visit_id)
            else:
              visit_id = request.POST.get('visit_id')
            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)

            visit_complaint_formset_prefix="edit_visit_complaints_"+str(visit_id)
            vasc_exam_formset_prefix = "edit_vasc_exam_"+str(visit_id)

            visit_complaint_obj = VisitComplaint.objects.filter(
                visit_detail=visit_detail_obj)

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Error ! Invalid Request Parameters. ")
        except (VisitDetail.DoesNotExist):
            raise Http404("Requested Visit Does not exist.")

        success = False
        error_message = None

        if visit_complaint_obj and visit_hpi_obj and visit_ros_obj:
            #visit_complaint_form   = VisitComplaintForm(request.POST, instance = visit_complaint_obj[0])
            complaint_formset_auto_id = "id_"+visit_complaint_formset_prefix + \
                "_edit_visit_complaint_" + str(id)
            complaint_total_form_auto_id = "id_"+ visit_complaint_formset_prefix+\
              "-TOTAL_FORMS_edit_visit_complaint_" + str(id)
            #VisitComplaintFormset = modelformset_factory(VisitComplaint, form = VisitComplaintForm)
            visit_complaint_formset = VisitComplaintFormset(
                request.POST, queryset=visit_complaint_obj,
                prefix=visit_complaint_formset_prefix,
                auto_id=complaint_formset_auto_id)

            if visit_complaint_formset.is_valid()    :                

                saved_visit_complaints = visit_complaint_formset.save(commit=False)

                for complaint in saved_visit_complaints:
                    complaint.visit_detail = saved_visit
                    complaint.save()
                success = True
                error_message = "Visit Edited Successfully"

            else:
                success = False
                error_message = ''' <h4>Visit Could not be Saved.
                            Please check the forms for errors</h4>
                        '''

                for form in visit_complaint_formset:
                    errors += aumodelformerrorformatter_factory(form)

                error_message += ('\n' + errors)

            data = {'success': success,
                    'error_message': error_message
                    }
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

        else:
            raise Http404(
                "ERROR!  The visit has not associated complaints, HPI or ROS to edit")
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_complaint_del(request, visit_complaint_id = None):
    
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

        except (VisitComplaint.DoesNotExist):
            raise Http404("Requested Visit Complaint Does not exist.")

        else:
            success = False
            error_message = "Insufficient Permission. Could not delete."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')

    else:
        raise Http404(" Error ! Unsupported Request..")


#

@login_required
def visit_complaint_add(request, visit_id=None):
    user = request.user
    success = False
    error_message = "Complaint Added Successfully"
    form_errors = []
    try:
        if visit_id :
          visit_id = int(visit_id)
        else:
          visit_id = int(request.GET.get('visit_id'))
        visit_detail_obj = VisitDetail.objects.get(pk= visit_id)
        patient_detail_obj = visit_detail_obj.patient_detail
        visit_complaint_objs = VisitComplaint.objects.filter(
            visit_detail=visit_detail_obj)
        visit_complaint_obj = VisitComplaint(visit_detail=visit_detail_obj)
        VisitComplaintFormset = modelformset_factory(
            VisitComplaint, form=VisitComplaintForm, extra=1)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
        raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
        raise Http404("Requested Visit Does not exist.")

    if request.method == "GET" and request.is_ajax():
        print "Received GET request to add Visit Complaints "
    # visit_complaint_form = VisitComplaintForm(instance = visit_complaint_obj,
                                                  # auto_id  =
                                                  # "id_new_visit_complaint"+
                                                  # str(id)+"_%s")
        visit_complaint_formset = VisitComplaintFormset(
            queryset=visit_complaint_objs)
        #print visit_complaint_formset
        variable = RequestContext(
            request, {'user': user,
                      'visit_detail_obj': visit_detail_obj,
                      'visit_complaint_formset': visit_complaint_formset,
                      'patient_detail_obj': patient_detail_obj
                      })
        return render_to_response('visit_complaints/add.html', variable)

    if request.method == "POST" and request.is_ajax():
        print "Received POST request to add Visit complaints ..."
        #visit_complaint_form = VisitComplaintForm(request.POST, instance = visit_complaint_obj)
        visit_complaint_formset = VisitComplaintFormset(request.POST)

        if visit_complaint_formset.is_valid():
            saved_visit_complaint = visit_complaint_formset.save(commit=False)
            for complaint in saved_visit_complaint:
                complaint.visit_detail = saved_visit
                complaint.save()

            success = True
        else:
            success = False
            error_message = '''Error! Complaint Could not be added.
                          Please check the forms for errors
                      '''
        data = {'success': success,
                'error_message': error_message
                }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_complaint_edit(request, complaint_id=None):
    pass


@login_required
def visit_complaint_del(request, complaint_id=None):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        if user.has_perm('visit.delete_visitcomplaint'):
            try:
                if complaint_id : 
                  complaint_id = int(complaint_id)
                else:
                  complaint_id = int(request.GET.get('complaint_id'))
                visit_complaint_obj = VisitComplaint.objects.get(pk=complaint_id)
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
            return HttpResponse(json, content_type='application/json')
        else:
            success = False
            error_message = "Insufficient Permission. Could not delete."
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
    else:
        raise Http404(" Error ! Unsupported Request..")