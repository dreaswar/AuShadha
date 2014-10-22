#################################################################################
# Project      : AuShadha
# Description  : Views for DrugBankCaDrugs
# Author       : Dr.Easwar T.R 
# Date         : 04-10-2013
# License      : GNU-GPL Version 3, See LICENSE.txt 
################################################################################

import os
import sys
from datetime import datetime, date, time
import zipfile

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid


from .models import DrugBankCaDrugs
 
# Views start here -----------------------------------------

ZIP_FILE_PATH = 'registry/drug_db/drugbankca/drugbank_scraper/data/drugbank_tables.zip'

@login_required
def get_drugbankca_publications(request):

    if request.method == 'GET':
       user = request.user
       variable = RequestContext(request, {'user': user})
       return render_to_response('drugbankca/publications.html', variable)
    else:  
       raise Http404("Bad Request Method")

@login_required
def drugbankcadrugs_json_for_a_drug(request,drug_id=None):
    pass


@login_required
def drugbankcadrugs_summary_by_drug_id(request,drug_id):
    pass


@login_required
def drugbankcadrugs_summary_by_drug_name(request):

  if request.method == 'GET' and request.is_ajax():
    try:
        drug_name = request.GET.get("drug_name")
        active_ingredient = request.GET.get("active_ingredient")
        print("Requesting for Drug: " + drug_name + " with active ingredient " + active_ingredient)
        drugbankca_drug = DrugBankCaDrugs.objects.filter(drug_name__iexact = drug_name)
    except(KeyError,NameError,AttributeError):
        return HttpResponse("Drug / Active ingredient Not Listed (OR) \n \
                             You have supplied invalid drug name / active ingredient")
    if len(drugbankca_drug) == 0:
         print(drugbankca_drug)
         drugbankca_drug = DrugBankCaDrugs.objects.filter(drug_name__iexact = active_ingredient)
         print(drugbankca_drug)
         if len(drugbankca_drug) == 0:
             drugbankca_drug = DrugBankCaDrugs.objects.filter(drug_name__icontains = active_ingredient)
             if len(drugbankca_drug) ==0:
                 return HttpResponse("Drug / Active ingredient Not Listed in DrugBankCa. \n \
                                      For latest updates please search http://drugbankca.ca")
    drugbankca_drug = drugbankca_drug[0]
    drug_id = drugbankca_drug.drug_id
#    try:
    zip_tables = zipfile.ZipFile(ZIP_FILE_PATH)
    print("Trying to find document with ID: " + drug_id)
    document = zip_tables.open(drug_id)           
#    except(IOError):
#        print("Drug with ID: "+drug_id + " not found")
#        return HttpResponse("Drug / Active ingredient Not Listed (OR) \n  \
#                             A bad file path may have been supplied by you")
    html = document.read()
    document.close()
    return HttpResponse(html)

  else:
     return Http404("Bad Request Method")


@login_required
def drugbankcadrugs_search_by_drug_name(request):

    if request.method == "GET" and request.is_ajax():
        try:
            drug_name = request.GET.get('drug_name')
        except(KeyError,NameError,TypeError,ValueError):
            raise Http404("Bad Request Parameters")

        if drug_name == '*' or drug_name == ' ':
            drug_obj = DrugBankCaDrugs.objects.all()[:25]
        else:
            drug_name  = drug_name.split('*')[0]
            drug_obj = DrugBankCaDrugs.objects.filter(drug_name__istartswith = drug_name)[:25]

        if len(drug_obj) == 0:
            drug_obj = DrugBankCaDrugs.objects.filter(drug_name__icontains = drug_name)[:25]
        data = []
  	for d in drug_obj:
	   data_to_append = {}
  	   data_to_append['drug_name'] = d.drug_name.title()
	   data_to_append['dosage'] = ''
	   data_to_append['id'] = d.pk
           data_to_append['absolute_url'] = ''
	   data_to_append['active_ingredient'] = ''
           data_to_append['url'] = reverse('drugbankcadrugs_summary_by_drug_name')+\
                                          "?drug_name="+d.drug_name               +\
                                          "&active_ingredient="+d.drug_name
	   data.append(data_to_append)
           json_data = json.dumps(data)
	   return HttpResponse(jsondata, content_type = 'application/json')

    else:
        raise Http404("Bad Request Method")



@login_required
def drugbankcadrugs_search(request):
    pass

