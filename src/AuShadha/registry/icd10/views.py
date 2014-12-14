################################################################################
# Project      : AuShadha
# Description  : Views for Demographics
# Author       : Dr.Easwar T.R 
# Date         : 04-10-2013
# License      : GNU-GPL Version 3, See LICENSE.txt 
################################################################################

import os
import sys
from datetime import datetime, date, time

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
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory


from .models import Chapter, Section, Diagnosis


# Views start here -----------------------------------------

@login_required
def get_all_chapters_json(request):
    user = request.user

    if request.method == 'GET':
        all_chapters = Chapter.objects.all()
        data = []
        for d in all_chapters:
           data_to_append = {}
           data_to_append['chapter_name'] = d.chapter_name.title()
           data_to_append['chapter_desc'] = d.chapter_desc
           data_to_append['includes'] = d.includes
           data_to_append['useAdditionalCode'] = d.useAdditionalCode
           data_to_append['excludes1'] = d.excludes1
           data_to_append['exlcludes2'] = d.excludes2
           data_to_append['sectionIndex'] = d.sectionIndex
           data.append(data_to_append)

        jsondata = json.dumps(data)
        return HttpResponse(jsondata, content_type = 'application/json')

    else:
       return Http404("Bad Request Method")   


@login_required
def get_all_section_json(request):
    pass



@login_required
def get_all_diagnosis_json(request):

    user = request.user

    if request.method == 'GET':
        all_diagnosis = Diagnosis.objects.all()
        data = []
        for d in all_diagnosis:
           data_to_append = {}
           data_to_append['diag_name'] = d.diag_name.title()
           data_to_append['diag_code'] = d.diag_code
           data.append(data_to_append)

        jsondata = json.dumps(data)
        return HttpResponse(jsondata, content_type = 'application/json')

    else:
       return Http404("Bad Request Method")


@login_required
def icd10_diagnosis_search(request):
    
    import random

    user = request.user
    search_for = request.GET.get('name')

    if request.method == 'GET':


        if search_for == '*' or search_for == ' ':
          diagnosis = Diagnosis.objects.all()[:100]

        else:
           search_for = search_for.split('*')[0]
           print "Searching for ICD10 code containing ", search_for
           diagnosis = Diagnosis.objects.filter(diag_code__icontains = search_for)[:100]

        data = []
        print diagnosis
	for d in diagnosis:
	   data_to_append = {}
	   data_to_append['diag_name'] = d.diag_name.title()
	   data_to_append['diag_code'] = d.diag_code
	   data_to_append['name'] = '%s - %s ' %(d.diag_name, d.diag_code)
	   data.append(data_to_append)
        jsondata = json.dumps(data)
        print json
	return HttpResponse(jsondata, content_type = 'application/json')

    else:
       return Http404("Bad Request Method")



@login_required
def icd10_chapter_json(request):
    return get_all_chapters_json(request)



@login_required
def get_sections_for_chapter(request, chapter_id, output='html'):

    if request.method == 'GET':
      user = request.user

      try:
        chapter_id = int(chapter_id)
        chapter_obj = Chapter.objects.get(pk = chapter_id)
        sections = Section.objects.filter(chapter_fk = chapter_obj)

      except (ValueError, NameError, AttributeError, TypeError):
        raise Exception("Invalid Attributes")

      except (Chapter.DoesNotExist):
        raise Exception("Requested Chapter Does Not Exist")

      if output == 'json':
	      data = []
	      for section in sections:
		 data_to_append = {}
		 data_to_append['sec_id'] = section.sec_id
		 data_to_append['diag_id'] = section.diag_id
		 data_to_append['desc'] = section.desc
		 data.append(data_to_append)
	     
	      jsondata = json.dumps(data)
	      return HttpResponse(jsondata, content_type = 'application/json')

      elif output == 'html':
          variable = RequestContext(request, {'user': user, 'sections': sections, 'chapter_obj': chapter_obj} )
          return render_to_response('icd10/sections.html', variable)

      elif output == 'tree':
          print "Received request to build ICD 10 Sections tree widget"
          from .dijit_widgets.tree import ICD10Tree
          path = 'registry/icd10/dijit_widgets/sections_tree.yaml'
          var = {'request': request, 
                 'user': user, 
                 'sections': sections, 
                 'chapter_obj': chapter_obj, 
                 'yaml_path': path, 
                 'node_name': 'sections'
                }
          tree = ICD10Tree(**var)()
          return HttpResponse(tree, content_type= 'application/json')
          

    else:
      raise Http404("Bad Request")


@login_required
def get_diagnosis_for_section(request, section_id, output = 'html'):

    if request.method == 'GET':
      user = request.user

      try:
        section_id = int(section_id)
        section_obj = Section.objects.get(pk = section_id)
        diagnosis = Diagnosis.objects.filter(section_fk = section_obj)

      except (ValueError, NameError, AttributeError, TypeError):
        raise Exception("Invalid Attributes")

      except (Section.DoesNotExist):
        raise Exception("Requested Section Does Not Exist")

      if output == 'json':
	      data = []
	      for diag in diagnosis:
		 data_to_append = {}
		 data_to_append['diag_name'] = diag.diag_name
		 data_to_append['diag_code'] = diag.diag_code
		 data.append(data_to_append)
	     
	      jsondata = json.dumps(data)
	      return HttpResponse(jsondata, content_type = 'application/json')

      elif output == 'html':
          variable = RequestContext(request, {'user': user, 'diagnosis': diagnosis, 'section_obj': section_obj} )
          return render_to_response('icd10/diagnosis.html', variable)

      elif output == 'tree':
          print "Received request to build ICD 10 Diagnosis tree widget"
          from .dijit_widgets.tree import ICD10Tree
          path = 'registry/icd10/dijit_widgets/diagnosis_tree.yaml'
          var = {'request': request, 
                 'user': user, 
                 'diagnosis': diagnosis, 
                 'section_obj': section_obj, 
                 'yaml_path': path, 
                 'node_name': 'diagnosis'
                }
          tree = ICD10Tree(**var)()
          return HttpResponse(tree, content_type= 'application/json')
          

    else:
      raise Http404("Bad Request")






