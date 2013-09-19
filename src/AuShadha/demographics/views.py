# --------------------------------------------------------------
# Views for Patient contact and details display and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date: 26-09-2010
# ---------------------------------------------------------------

#import wx
import os
import sys

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

from django.core.paginator import Paginator

from django.utils import simplejson
from django.core import serializers
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder


from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib.sites.models import get_current_site
import urlparse

# General Module imports-----------------------------------
from datetime import datetime, date, time


# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL

from core.serializers.data_grid import generate_json_for_datagrid

from patient.models import PatientDetail
from demographics.models import Contact, Phone, EmailAndFax, Demographics,\
                                ContactForm, PhoneForm, EmailAndFaxForm, DemographicsForm



# Views start here -----------------------------------------

@login_required
def contact_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return patient_contact_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")
    contact_obj = Contact.objects.filter(
        patient_detail=patient_detail_obj)
    json = generate_json_for_datagrid(contact_obj)
    print json
    return HttpResponse(json, content_type="application/json")

@login_required
def contact_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                contact_obj = Contact(
                    patient_detail=patient_detail_obj)
                contact_add_form = ContactForm(
                    instance=contact_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "contact_add_form": contact_add_form,
                                           "contact_obj": contact_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('demographics/contact/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                contact_obj = Contact(
                    patient_detail=patient_detail_obj)
                contact_add_form = ContactForm(
                    request.POST, instance=contact_obj)
                if contact_add_form.is_valid():
                    contact_object = contact_add_form.save(
                    )
                    success = True
                    error_message = "Contact Saved Successfully"
                    form_errors = None
                    addData = {
                        "id": contact_object.id,
                        'pat_id': contact_object.patient_detail.id,
                        "address_type": contact_object.address_type,
                        "address": contact_object.address,
                        "city": contact_object.city,
                        "state": contact_object.state,
                        "country": contact_object.country,
                        "pincode": contact_object.pincode,
                        "edit": contact_object.get_edit_url(),
                        "del": contact_object.get_del_url(),
                    }
                    data = {"success": success,
                            "error_message": error_message,
                            "form_errors": form_errors,
                            "addData": addData
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error:: Contact could not be added."
                    form_errors = ''
                    for error in contact_add_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def contact_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                contact_obj = Contact.objects.get(pk=id)
                contact_edit_form = ContactForm(
                    instance=contact_obj)
                patient_detail_obj = contact_obj.patient_detail
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "contact_edit_form": contact_edit_form,
                                           "contact_obj": contact_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientContact.DoesNotExist:
                raise Http404(
                    "BadRequest: Contact Data Does Not Exist")
            return render_to_response('demographics/contact/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                contact_obj = Contact.objects.get(pk=id)
                patient_detail_obj = contact_obj.patient_detail
                contact_edit_form = ContactForm(
                    request.POST, instance=contact_obj)
                if patient_contact_edit_form.is_valid():
                    contact_object = contact_edit_form.save()
                    success = True
                    error_message = "Contact Saved Successfully"
                    form_errors = None
                    success = True
                    error_message = "Contact Saved Successfully"
                    form_errors = None
                    data = {"success": success,
                            "error_message": error_message,
                            "form_errors": form_errors,
                            "id": contact_object.id,
                            'pat_id': contact_object.patient_detail.id,
                            "address_type": contact_object.address_type,
                            "address": contact_object.address,
                            "city": contact_object.city,
                            "state": contact_object.state,
                            "country": contact_object.country,
                            "pincode": contact_object.pincode,
                            "edit": contact_object.get_edit_url(),
                            "del": contact_object.get_del_url()
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error:: Contact could not be added."
                    form_errors = ''
                    for error in contact_edit_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success'               : success,
                            'error_message' : error_message,
                            'form_errors': form_errors
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except Contact.DoesNotExist:
                raise Http404(
                    "BadRequest: Requested Contact DoesNotExist")
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def contact_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                contact_obj = Contact.objects.get(pk=id)
                patient_detail_obj = contact_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Contact.DoesNotExist:
                raise Http404(
                    "BadRequest: Patient contact Data Does Not Exist")
            contact_obj.delete()
            success = True
            error_message = "contact Data Deleted Successfully"
            data = {
                'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")




@login_required
def phone_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return phone_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")
    phone_obj = Phone.objects.filter(
        patient_detail=patient_detail_obj)
    json = generate_json_for_datagrid(phone_obj)
    return HttpResponse(json, content_type="application/json")


@login_required
def guardian_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return guardian_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
        raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")
    guardian_obj = Guardian.objects.filter(
        patient_detail=patient_detail_obj)
    json = generate_json_for_datagrid(guardian_obj)
    return HttpResponse(json, content_type="application/json")


@login_required
def email_and_fax_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                email_and_fax_obj = EmailAndFax(
                    patient_detail=patient_detail_obj)
                email_and_fax_add_form = EmailAndFaxForm(
                    instance=email_and_fax_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "email_and_fax_add_form": email_and_fax_add_form,
                                           "email_and_fax_obj": email_and_fax_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('demographics/email_and_fax/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                email_and_fax_obj = EmailAndFax(
                    patient_detail=patient_detail_obj)
                email_and_fax_add_form = EmailAndFaxForm(
                    request.POST, instance=email_and_fax_obj)
                if email_and_fax_add_form.is_valid():
                    email_and_fax_object = email_and_fax_add_form.save(
                    )
                    success = True
                    error_message = "Email And Fax Saved Successfully"
                    form_errors = None
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error:: Email and Fax detail could not be added."
                    form_errors = ''
                    for error in email_and_fax_add_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def email_and_fax_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                email_and_fax_obj = EmailAndFax(pk=id)
                email_and_fax_edit_form = EmailAndFaxForm(
                    instance=email_and_fax_obj)
                patient_detail_obj = email_and_fax_obj.patient_detail
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "email_and_fax_edit_form": email_and_fax_edit_form,
                                           "email_and_fax_obj": email_and_fax_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except EmailAndFax.DoesNotExist:
                raise Http404(
                    "BadRequest: Email and Fax Data Does Not Exist")
            return render_to_response('demographics/email_and_fax/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                email_and_fax_obj = EmailAndFax.objects.get(
                    pk=id)
                patient_detail_obj = email_and_fax_obj.patient_detail
                email_and_fax_edit_form = EmailAndFaxForm(
                    request.POST, instance=email_and_fax_obj)
                if email_and_fax_edit_form.is_valid():
                    email_and_fax_object = email_and_fax_edit_form.save(
                    )
                    return HttpResponseRedirect(request.get_full_path())
                else:
                    variable = RequestContext(request,
                                              {"email_and_fax_edit_form": email_and_fax_edit_form,
                                               "user": user,
                                               'patient_detail_obj': patient_detail_obj
                                               })
                    return render_to_response("demographics/email_and_fax/edit.html", variable)
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except EmailAndFax.DoesNotExist:
                raise Http404(
                    "BadRequest: Requested Email and Fax DoesNotExist")
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def email_and_fax_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                email_and_fax_obj = EmailAndFax.objects.get(pk=id)
                patient_detail_obj = email_and_fax_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except EmailAndFax.DoesNotExist:
                raise Http404(
                    "BadRequest: Email and Fax Data Does Not Exist")
            email_and_fax_obj.delete()
            success = True
            error_message = "Email and Fax Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")



@login_required
def guardian_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                guardian_obj = Guardian(
                    patient_detail=patient_detail_obj)
                guardian_add_form = GuardianForm(
                    instance=guardian_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "guardian_add_form": guardian_add_form,
                                           "guardian_obj": guardian_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('demographics/guardian/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                guardian_obj = Guardian(
                    patient_detail=patient_detail_obj)
                guardian_add_form = GuardianForm(
                    request.POST, instance=guardian_obj)
                if guardian_add_form.is_valid():
                    guardian_object = guardian_add_form.save(
                    )
                    success = True
                    error_message = "Guardian data Saved Successfully"
                    form_errors = None
                    addData = {
                        "id": guardian_object.id,
                        "edit": guardian_object.get_edit_url(),
                        "del": guardian_object.get_del_url(),
                        "guardian_name": guardian_object.guardian_name,
                        "relation_to_guardian": guardian_object.relation_to_guardian,
                        "guardian_phone": guardian_object.guardian_phone
                    }
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors,
                            "addData": addData
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error:: Guardian could not be added."
                    form_errors = ''
                    for error in guardian_add_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def guardian_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                guardian_obj = Guardian.objects.get(
                    pk=id)
                guardian_edit_form = GuardianForm(
                    instance=guardian_obj)
                patient_detail_obj = guardian_obj.patient_detail
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "guardian_edit_form": guardian_edit_form,
                                           "guardian_obj": guardian_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientContact.DoesNotExist:
                raise Http404(
                    "BadRequest: Patient guardian Data Does Not Exist")
            return render_to_response('demographics/guardian/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                guardian_obj = Guardian.objects.get(
                    pk=id)
                patient_detail_obj = guardian_obj.patient_detail
                guardian_edit_form = GuardianForm(
                    request.POST, instance=guardian_obj)
                if guardian_edit_form.is_valid():
                    guardian_object = guardian_edit_form.save(
                    )
                    success = True
                    error_message = "Guardian data Saved Successfully"
                    form_errors = None
                    addData = {
                        "id": guardian_object.id,
                        "edit": guardian_object.get_edit_url(),
                        "del": guardian_object.get_del_url(),
                        "guardian_name": guardian_object.guardian_name,
                        "relation_to_guardian": guardian_object.relation_to_guardian,
                        "guardian_phone": guardian_object.guardian_phone
                    }
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors,
                            "addData": addData
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error:: Guardian could not be added."
                    form_errors = ''
                    for error in guardian_edit_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientContact.DoesNotExist:
                raise Http404(
                    "BadRequest: Requested Patient guardian DoesNotExist")
        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def guardian_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                guardian_obj = Guardian.objects.get(pk=id)
                patient_detail_obj = guardian_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Guardian.DoesNotExist:
                raise Http404(
                    "BadRequest: Guardian Data Does Not Exist")
            guardian_obj.delete()
            success = True
            error_message = "Guardian Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")




@login_required
def phone_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                phone_obj = Phone(
                    patient_detail=patient_detail_obj)
                phone_add_form = PhoneForm(
                    instance=phone_obj)
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "phone_add_form": phone_add_form,
                                           "phone_obj": phone_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
            return render_to_response('demographics/phone/add.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                phone_obj = Phone(
                    patient_detail=patient_detail_obj)
                phone_add_form = PhoneForm(
                    request.POST, instance=phone_obj)
                if phone_add_form.is_valid():
                    phone_obj = phone_add_form.save()
                    success = True
                    error_message = "Phone Data Added Successfully"
                    addData = {
                        "id": phone_obj.id,
                        "phone_type": phone_obj.phone_type,
                        "ISD_Code": phone_obj.ISD_Code,
                        "STD_Code": phone_obj.STD_Code,
                        "phone": phone_obj.phone,
                        "edit": phone_obj.get_edit_url(),
                        "del": phone_obj.get_del_url()
                    }
                    data = {'success': success,
                            'error_message': error_message,
                            "form_errors": None,
                            "addData": addData
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error Occured. Phone data could not be added."
                    form_errors = ''
                    for error in phone_add_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404(
                "BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))


@login_required
def phone_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                phone_obj = Phone.objects.get(pk=id)
                phone_edit_form = PhoneForm(
                    instance=phone_obj)
                patient_detail_obj = phone_obj.patient_detail
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "phone_edit_form": phone_edit_form,
                                           "phone_obj": phone_obj,
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Phone.DoesNotExist:
                raise Http404("BadRequest: Phone Data Does Not Exist")
            return render_to_response('demographics/phone/edit.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                phone_obj = Phone.objects.get(pk=id)
                phone_edit_form = PhoneForm(
                    request.POST, instance=phone_obj)
                patient_detail_obj = phone_obj.patient_detail
                if phone_edit_form.is_valid():
                    phone_obj = phone_edit_form.save()
                    success = True
                    error_message = "Phone Data Edited Successfully"
                    data = {'success': success,
                            'error_message': error_message,
                            "form_errors": None,
                            "id": phone_obj.id,
                            "phone_type": phone_obj.phone_type,
                            "ISD_Code": phone_obj.ISD_Code,
                            "STD_Code": phone_obj.STD_Code,
                            "phone": phone_obj.phone,
                            "edit": phone_obj.get_edit_url(),
                            "del": phone_obj.get_del_url()
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error Occured. Phone data could not be added."
                    form_errors = ''
                    for error in phone_edit_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except Phone.DoesNotExist:
                raise Http404(
                    "BadRequest: Requested Phone DoesNotExist")
        else:
            raise Http404(
                "BadRequest: Unsupported Request Method. request's AJAX status was:: ", request.is_ajax())


@login_required
def phone_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                phone_obj = Phone(pk=id)
                patient_detail_obj = phone_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Phone.DoesNotExist:
                raise Http404("BadRequest: Phone Data Does Not Exist")
            phone_obj.delete()
            success = True
            error_message = "Phone Data Deleted Successfully"
            data = {'success': success, 'error_message': error_message}
            json = simplejson.dumps(data)
            return HttpResponse(json, content_type='application/json')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")


@login_required
def demographics_json(request):
    try:
        action = unicode(request.GET.get('action'))
        id = int(request.GET.get('patient_id'))
        if action == 'add':
            return demographics_add(request, id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
        demographics_obj = Demographics.objects.filter(
            patient_detail=patient_detail_obj)
        json = generate_json_for_datagrid(demographics_obj)
        return HttpResponse(json, content_type="application/json")
    except(AttributeError, NameError, TypeError, ValueError, KeyError):
      raise Http404("ERROR:: Bad request.Invalid arguments passed")
    except(PatientDetail.DoesNotExist):
        raise Http404("ERROR:: Patient requested does not exist.")

@login_required
def demographics_add(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
                demographics_obj = Demographics.objects.filter(
                    patient_detail=patient_detail_obj)
                if demographics_obj:
                    demographics_obj = demographics_obj[0]
                    demographics_form = DemographicsForm(
                        instance=demographics_obj)
                    variable = {'user': user,
                                'patient_detail_obj': patient_detail_obj,
                                'demographics_obj': demographics_obj,
                                'demographics_form': demographics_form,
                                'button_label': 'Edit',
                                'action': demographics_obj.get_edit_url(),
                                'canDel': True,
                                "addUrl": None,
                                'editUrl': demographics_obj.get_edit_url(),
                                'delUrl': demographics_obj.get_del_url()
                                }
                else:
                    demographics_obj = Demographics(
                        patient_detail=patient_detail_obj)
                    demographics_form = DemographicsForm(
                        instance=demographics__obj)
                    variable = RequestContext(request,
                                              {"user": user,
                                               "patient_detail_obj": patient_detail_obj,
                                               "demographics_form": demographics_form,
                                               "demographics_obj": demographics_obj,
                                               'button_label': "Add",
                                               "action": patient_detail_obj.get_demographics__add_url(),
                                               "addUrl": patient_detail_obj.get_demographics__add_url(),
                                               'canDel': False,
                                               'editUrl': None,
                                               'delUrl': None
                                               })
                return render_to_response('patient/demographics/add_or_edit_form.html', variable)
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Patient Data Does Not Exist")
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(
                    pk=id)
                demographics_obj = Demographics(
                    patient_detail=patient_detail_obj)
                demographics_form = DemographicsForm(
                    request.POST, instance=demographics_obj)
                if demographics_form.is_valid():
                    try:
                        demographics_obj = demographics_form.save(
                        )
#            json              = generate_json_for_datagrid(demographics_obj)
                        success = True
                        error_message = "Demographics Data Added Successfully"
                        form_errors = ''
                        data = {'success': success,
                                'error_message': error_message,
                                'form_errors': form_errors,
                                'canDel': True,
                                'addUrl': None,
                                'editUrl': demographics_obj.get_edit_url(),
                                'delUrl': demographics_obj.get_del_url(),
                                }
                        json = simplejson.dumps(data)
                        return HttpResponse(json, content_type='application/json')
                    except (DemographicsDataExistsError):
                        success = False
                        error_message = "Demographics Data Already Exists ! Cannot add more.."
                        form_errors = ''
                        data = {'success': success,
                                'error_message': error_message,
                                'form_errors': form_errors
                                }
                        json = simplejson.dumps(data)
                        return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error Occured. DemographicsData data could not be added."
                    form_errors = ''
                    for error in demographics_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors
                            }
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except PatientDetail.DoesNotExist:
                raise Http404("BadRequest: Requested Patient DoesNotExist")
        else:
            raise Http404(
                "BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))


@login_required
def demographics_edit(request, id):
    if request.user:
        user = request.user
        if request.method == "GET" and request.is_ajax():
            try:
                id = int(id)
                demographics_obj = Demographics.objects.get(
                    pk=id)
                demographics_form = DemographicsForm(
                    instance=demographics_obj)
                patient_detail_obj = demographics_obj.patient_detail
                variable = RequestContext(request,
                                          {"user": user,
                                           "patient_detail_obj": patient_detail_obj,
                                           "demographics_form": demographics_form,
                                           "demographics_obj": demographics_obj,
                                           'action': demographics_obj.get_edit_url(),
                                           'button_label': "Edit",
                                           'canDel': True,
                                           'addUrl': None,
                                           'editUrl': demographics_obj.get_edit_url(),
                                           'delUrl': demographics_obj.get_del_url(),
                                           })
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Demographics.DoesNotExist:
                raise Http404(
                    "BadRequest: Patient DemographicsData Data Does Not Exist")
            return render_to_response('patient/demographics/add_or_edit_form.html', variable)
        elif request.method == 'POST' and request.is_ajax():
            try:
                id = int(id)
                demographics_obj = Demographics.objects.get(
                    pk=id)
                demographics_form = DemographicsForm(
                    request.POST, instance=demographics__obj)
                patient_detail_obj = demographics_obj.patient_detail
                if demographics_form.is_valid():
                    demographics_obj = demographics_form.save()
                    success = True
                    error_message = "Demographics Data Edited Successfully"
                    form_errors = ''
                    data = {'success': success,
                            'error_message': error_message,
                            'form_errors': form_errors
                            }
#          data             = generate_json_for_datagrid(demographics_obj)
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
                else:
                    success = False
                    error_message = "Error Occured. Demographics Data data could not be added."
                    form_errors = ''
                    for error in demographics_form.errors:
                        form_errors += '<p>' + error + '</p>'
                    data = {'success': success, 'error_message': error_message, 'form_errors':
                            form_errors}
                    json = simplejson.dumps(data)
                    return HttpResponse(json, content_type='application/json')
            except ValueError or AttributeError or TypeError:
                raise Http404("BadRequest: Server Error")
            except Demographics.DoesNotExist:
                raise Http404(
                    "BadRequest: Requested Patient Demographics Data DoesNotExist")
        else:
            raise Http404(
                "BadRequest: Unsupported Request Method. request's AJAX status was:: ", request.is_ajax())


@login_required
def demographics_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                demographics_obj = Demographics.objects.get(
                    pk=id)
                patient_detail_obj = demographics_obj.patient_detail
            except TypeError or ValueError or AttributeError:
                raise Http404("BadRequest")
            except Demographics.DoesNotExist:
                raise Http404(
                    "BadRequest: Patient Demographics Data Does Not Exist")
            demographics_obj.delete()
            success = True
            error_message = "Demographics Data Deleted Successfully"
            data = {'success': success,
                    'error_message': error_message,
                    'addUrl': patient_detail_obj.get_demographics__add_url(),
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