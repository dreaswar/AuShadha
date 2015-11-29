##########################################################################
# Physical Examination Views for AuShadha
# Takes care of all the Physical Examination Related Data.
# Author    : Dr.Easwar T.R
# Copyright : 2012
# Date      : 2012-12-31
# License   : GNU-GPL Version 3
##########################################################################


# General Module imports-----------------------------------
import StringIO
#import ho.pisa as pisa
#from reportlab.pdfgen import canvas
from datetime import datetime, date, time
import yaml
import importlib

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.template import RequestContext
#from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import json
#from django.core.context_processors  import csrf
#from django.views.decorators.csrf    import csrf_exempt
from django.template import loader, Context

# Application Specific Model Imports-----------------------

#from AuShadha.settings import LOGIN_URL
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.utilities.forms import AuModelFormErrorFormatter, aumodelformerrorformatter_factory

#from patient.models import *
#from patient.views import *
#from admission.models import *
#from visit.models import *

PatientDetail = UI.get_module("PatientRegistration")
AdmissionDetail = UI.get_module("Admission")
VisitDetail = UI.get_module("OPD_Visit")

from .models import VitalExam, GenExam, SysExam, NeuroExam, VascExam, MusculoSkeletalExam
from .models import VitalExamForm, GenExamForm, SysExamForm, NeuroExamForm, VascExamForm, MusculoSkeletalExamForm

from .utilities import visit_detail_has_exam

EXAM_NAME_MODEL_MAP = {
    'vitals': VitalExam,
    'sys': SysExam,
    'gen': GenExam,
    'neuro': NeuroExam,
    'vasc': VascExam,
    'musculoskeletal': MusculoSkeletalExam
}

EXAM_NAME_MODEL_FORM_MAP = {
    VitalExam: VitalExamForm,
    SysExam: SysExamForm,
    GenExam: GenExamForm,
    NeuroExam: NeuroExamForm,
    VascExam: VascExamForm,
    MusculoSkeletalExam: MusculoSkeletalExamForm
}


@login_required
def visit_phyexam_template(request, exam_name, visit_id=None):

    if request.method == "GET":
        user = request.user

        try:
            if visit_id:
                visit_id = int(visit_id)

            else:
                visit_id = int(request.GET.get('visit_id'))

            visit_detail_obj = VisitDetail.objects.get(pk=visit_id)
            exam_class = EXAM_NAME_MODEL_MAP.get(exam_name, '')

            if not exam_class:
                raise Http404("Invalid Exam Requested")

            try:
                template_file = 'visit_phyexam/%s_exam/template.html' % (
                    exam_name)
                #template = loader.get_template(template_file)
                variable = RequestContext(
                    request, {
                        'user': user, 'exam_name': exam_name, 'visit_detail_obj': visit_detail_obj})
                #rendered_html = template.render(variable)
                return render_to_response(template_file, variable)

            except Exception as ex:
                raise Http404("ERROR! ", ex)

        except (ValueError, KeyError, NameError, AttributeError):
            raise Http404("Invalid Exam template. ")

    else:
        raise Http404("Bad Request Method")


@login_required
def visit_phyexam_json(request, exam_name, visit_id=None):

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

    exam_class = EXAM_NAME_MODEL_MAP.get(exam_name, '')
    exam_form_class = EXAM_NAME_MODEL_FORM_MAP.get(exam_class, '')

    if not exam_class:
        raise Http404("Invalid Exam Requested")
    else:
        exam_objs = exam_class.objects.filter(visit_detail=visit_detail_obj)

    data = []

    if exam_objs:
        for obj in exam_objs:
            if not getattr(obj, 'urls', None):
                obj.save()
            data_to_append = {}
            data_to_append['id'] = obj.id
            data_to_append['edit'] = reverse(
                'visit_phyexam_edit', args=[
                    exam_name, obj.id])
            data_to_append['del'] = reverse(
                'visit_phyexam_del', args=[
                    exam_name, obj.id])

            if exam_name == 'vasc':
                data_to_append['location'] = obj.location
                data_to_append['side'] = obj.side
                data_to_append['character'] = obj.character

            elif exam_name == 'gen':
                pass

            elif exam_name == 'sys':
                pass

            elif exam_name == 'vitals':
                pass

            elif exam_name == 'neuro':
                pass

            data.append(data_to_append)

    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type="application/json")


@login_required
def visit_phyexam_list(request, exam_name, visit_id=None):
    pass


@login_required
def visit_phyexam_add(request, exam_name, visit_id=None):

    user = request.user
    try:
        if visit_id:
            visit_id = int(visit_id)
        else:
            visit_id = int(request.GET.get('visit_id'))
        visit_detail_obj = VisitDetail.objects.get(pk=visit_id)

    except (NameError, TypeError, ValueError, AttributeError, KeyError):
        raise Http404("Error! : Bad Parameters supplied ! ")

    except (VisitDetail.DoesNotExist):
        raise Http404("Error! : Requested Visit Does not Exist !")

    exam_class = EXAM_NAME_MODEL_MAP.get(exam_name, '')
    exam_form_class = EXAM_NAME_MODEL_FORM_MAP.get(exam_class, '')

    if not exam_class:
        raise Http404("Invalid Exam Requested")
    else:
        exam_obj = exam_class(visit_detail=visit_detail_obj)

    if not getattr(visit_detail_obj, 'urls', None):
        visit_detail_obj.save()

    def add_phyexam():
        if request.method == 'GET':
            exam_form = exam_form_class(instance=exam_obj, auto_id=False)
            variable = RequestContext(request,
                                      {'user': user,
                                       'visit_detail_obj': visit_detail_obj,
                                       'visit_phyexam_form': exam_form,
                                       'exam_obj': exam_obj,
                                       'visit_phyexam_action': 'add',
                                       'exam_name': exam_name})
            return render_to_response(
                'visit_phyexam/add_or_edit_form.html', variable)

        elif request.method == 'POST':
            exam_form = exam_form_class(request.POST, instance=exam_obj)

            if exam_form.is_valid():
                saved_exam = exam_form.save()
                saved_exam.visit_detail = visit_detail_obj
                saved_exam.save()
                success = True
                error_message = "Exam Saved Successfully"
                form_errors = None
                redirectUrl = reverse(
                    'visit_phyexam_edit', args=[
                        exam_name, saved_exam.id])

            else:
                success = False
                error_message = "Error! Exam Could not be saved"
                form_errors = aumodelformerrorformatter_factory(exam_form)
                error_message += "\n" + form_errors + "\n"
                redirectUrl = None

            data = {'success': success,
                    'error_message': error_message,
                    'form_errors': form_errors,
                    'redirectUrl': redirectUrl
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='json/application')

        else:
            raise Http404("Bad Request")

    if exam_name != 'vasc':

        if not visit_detail_has_exam(exam_class, visit_detail_obj):
            return add_phyexam()

        else:
            visit_phyexam_id = unicode(
                visit_detail_has_exam(
                    exam_class, visit_detail_obj)[0].id)
            return visit_phyexam_edit(request, exam_name, visit_phyexam_id)

    elif exam_name == 'vasc':
        return add_phyexam()


@login_required
def visit_phyexam_edit(request, exam_name, visit_phyexam_id=None):
    user = request.user
    exam_class = EXAM_NAME_MODEL_MAP.get(exam_name, '')
    exam_form_class = EXAM_NAME_MODEL_FORM_MAP.get(exam_class, '')

    try:
        if visit_phyexam_id:
            visit_phyexam_id = int(visit_phyexam_id)
        else:
            visit_phyexam_id = int(request.GET.get('visit_phyexam_id'))

        if not exam_class:
            raise Http404("Invalid Exam Requested")
        else:
            exam_obj = exam_class.objects.get(pk=visit_phyexam_id)
            visit_detail_obj = exam_obj.visit_detail

        if not getattr(exam_obj, 'urls', None):
            exam_obj.save()

        if not getattr(visit_detail_obj, 'urls', None):
            visit_detail_obj.save()

    except (NameError, TypeError, ValueError, AttributeError, KeyError):
        raise Http404("Error! : Bad Parameters supplied ! ")

    except (exam_class.DoesNotExist):
        raise Http404("Error! : Requested Examination Does not Exist !")

    if request.method == 'GET':
        exam_form = exam_form_class(instance=exam_obj, auto_id=False)
        variable = RequestContext(request,
                                  {'user': user,
                                   'visit_detail_obj': visit_detail_obj,
                                   'visit_phyexam_form': exam_form,
                                   'exam_obj': exam_obj,
                                   'visit_phyexam_action': 'edit',
                                   'exam_name': exam_name})
        if exam_name != 'vasc':
            return render_to_response(
                'visit_phyexam/add_or_edit_form.html', variable)
        else:
            return render_to_response(
                'visit_phyexam/snippets/forms/vasc.html', variable)

    elif request.method == 'POST':
        exam_form = exam_form_class(request.POST, instance=exam_obj)

        if exam_form.is_valid():
            saved_exam = exam_form.save()
            saved_exam.visit_detail = visit_detail_obj
            saved_exam.save()
            success = True
            error_message = "Exam Saved Successfully"
            form_errors = None
            redirectUrl = reverse(
                'visit_phyexam_edit', args=[
                    exam_name, saved_exam.id])

        else:
            success = False
            error_message = "Error! Exam Could not be saved"
            form_errors = aumodelformerrorformatter_factory(exam_form)
            error_message += "\n" + form_errors + "\n"
            redirectUrl = None

        data = {'success': success,
                'error_message': error_message,
                'form_errors': form_errors,
                'redirectUrl': redirectUrl
                }
        jsondata = json.dumps(data)
        return HttpResponse(jsondata, content_type='json/application')

    else:
        raise Http404("Bad Request")


@login_required
def visit_phyexam_del(request, exam_name, visit_phyexam_id=None):

    user = request.user
    exam_class = EXAM_NAME_MODEL_MAP.get(exam_name, '')
    exam_form_class = EXAM_NAME_MODEL_FORM_MAP.get(exam_class, '')

    try:
        if visit_phyexam_id:
            visit_phyexam_id = int(visit_phyexam_id)
        else:
            visit_phyexam_id = int(request.GET.get('visit_phyexam_id'))

        if not exam_class:
            raise Http404("Invalid Exam Requested")
        else:
            exam_obj = exam_class.objects.get(pk=visit_phyexam_id)
            visit_detail_obj = exam_obj.visit_detail

        # if not getattr(exam_obj,'urls',None):
            # exam_obj.save()

        # if not getattr(visit_detail_obj,'urls',None):
            # visit_detail_obj.save()

        if request.method == "GET" and request.is_ajax():

            exam_obj.delete()
            success = True
            error_message = "Successfully Deleted Exam"

            if exam_name != 'vasc':
                redirectUrl = reverse(
                    'visit_phyexam_add', args=[
                        exam_name, visit_detail_obj.id])
            else:
                redirectUrl = None

            data = {'success': success,
                    'error_message': error_message,
                    'redirectUrl': redirectUrl
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        else:
            raise Http404(" Error ! Unsupported Request..")

    except (NameError, TypeError, ValueError, AttributeError, KeyError):
        raise Http404("Error! : Bad Parameters supplied ! ")

    except (exam_class.DoesNotExist):
        raise Http404("Error! : Requested Examination Does not Exist !")
