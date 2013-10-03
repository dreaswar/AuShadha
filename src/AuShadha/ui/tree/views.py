################################################################################
# Project     : AuShadha
# Description : Views for UI Dijit Trees
# Author      : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date        : 03-10-2013
################################################################################


# General Module imports-----------------------------------
#from datetime import datetime, date, time

# General Django Imports----------------------------------
#from django.core.context_processors import csrf
#from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core import serializers
#from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder
#from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.settings import INSTALLED_APPS
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree

#from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
#from AuShadha.utilities.forms import aumodelformerrorformatter_factory
#from patient.models import PatientDetail, PatientDetailForm
#from AuShadha.apps.clinic.models import Clinic
#from demographics.models import Contact, Phone, Guardian, Demographics
#from medical_history.models import MedicalHistory
#from surgical_history.models import SurgicalHistory
#from social_history.models import SocialHistory
#from family_history.models import FamilyHistory
#from immunisation.models import Immunisation
#from allergy_list.models import Allergy
#from medication_list.models import MedicationList
#from admission.models import AdmissionDetail, AdmissionDetailForm
#from visit.models import VisitDetail, VisitImaging, VisitInv
#from obs_and_gyn.models import ObstetricHistoryDetail


@login_required
def patient(request):
    if request.method == "GET" and request.is_ajax():
            tree = DijitTree()
  
            history = DijitTreeNode({"name": "History",
                                          "type": "application",
                                          "id": "HISTORY"
                                        })

            medical_history = DijitTreeNode({"name": "Medical History",
                                                  "type": "medical_history_module",
                                                  "id": "MEDICAL_HISTORY"
                                                  })
            history.add_child_node(medical_history)

            surgical_history = DijitTreeNode({"name": "Surgical History",
                                                   "type": "surgical_history_module",
                                                   "id": "SURGICAL_HISTORY"
                                                 })
            history.add_child_node(surgical_history)

            family_history = DijitTreeNode({"name": "Family History",
                                                 "type": "family_history_module",
                                                 "id": "FAMILY_HISTORY"
                                                })
            history.add_child_node(family_history)

            social_history = DijitTreeNode({"name": "Social History",
                                                 "type": "social_history_module",
                                                 "id": "SOCIAL_HISTORY"
                                                })
            history.add_child_node(social_history)

            demographics = DijitTreeNode({"name": "Demographics",
                                              "type": "demographics_module",
                                              "id": "DEMOGRAPHICS"
                                              })
            history.add_child_node(demographics)

            tree.add_child_node(history)

            medication_list = DijitTreeNode({"name" : "Medications",
                                                  "type": "application",
                                                  "module_type": "medication_list_module",
                                                  "id" : "MEDICATIONS"
                                                })
            tree.add_child_node(medication_list)

            preventives = DijitTreeNode({"name": "Preventives",
                                            "type": "application",
                                            "id": "PREVENTIVES"
                                            })

            immunisation = DijitTreeNode({"name": "Immunisation",
                                              "type": "immunisation_module",
                                              "id": "IMMUNISATION"
                                              })
            preventives.add_child_node(immunisation)

            tree.add_child_node(preventives)

            #medical_preventives = DijitTreeNode({"name": "Medical",
                                                      #"type": "medical_preventives_module",
                                                      #"id": "MEDICAL_PREVENTIVES"
                                                      #})

            #surgical_preventives = DijitTreeNode({"name": "Surgical",
                                                        #"type": "surgical_preventives_module",
                                                        #"id": "SURGICAL_PREVENTIVES"
                                                      #})

            #obs_and_gyn_preventives = DijitTreeNode({"name": "Obs & Gyn",
                                                          #"type": "obs_and_gyn_preventives_module",
                                                          #"id": "OBS_PREVENTIVES"
                                                          #})

            #admission = DijitTreeNode({"name" : "AdmissionDetails"   , 
                                            #"type" :"application", 
                                            #"id"   :"ADM"
                                            #})

            #visit = DijitTreeNode({"name"  : "OPD Visits"          , 
                                        #"type":"application", 
                                        #"id":"VISIT"
                                        #})

            investigation = DijitTreeNode({"name": "Investigation", 
                                                "type": "application", 
                                                "id": "INV"
                                               })
            tree.add_child_node(investigation)

            imaging = DijitTreeNode({"name": "Imaging", 
                                          "type": "application", 
                                          "id": "IMAG"
                                         })
            tree.add_child_node(imaging)

            procedure = DijitTreeNode({"name": "Procedures", 
                                            "type": "application", 
                                            "id": "PROCEDURES"
                                            })
            tree.add_child_node(procedure)

            #calendar = DijitTreeNode({"name"  : "Calendar" , 
                                          #"type":"application", 
                                          #"id":"CAL" 
                                        #})

            #media = DijitTreeNode({"name": "Media", 
                                        #"type": "application", 
                                        #"id": "MEDIA"
                                      #})

            #documents = DijitTreeNode({"name": "Documents",
                                            #"type": "patient_documents_module",
                                            #"id": "DOCS"
                                          #})
            #images = DijitTreeNode({"name": "Images",
                                          #"type": "patient_images_module",
                                          #"id": "IMAGES"
                                        #})

            #coding = DijitTreeNode({"name": "Coding",
                                          #"type": "application",
                                          #"id": "CODING"
                                        #})

            #icd_10 = DijitTreeNode({"name": "ICD 10",
                                          #"type": "icd10_module",
                                          #"id": "ICD_10"
                                         #})

            #icd_10_pcs = DijitTreeNode({"name": "ICD 10 PC",
                                              #"type": "icd10_pcs_module",
                                              #"id": "ICD_10_PROCEDURE_CODES"
                                            #})

            json = tree.to_json()
            return HttpResponse(json, content_type="application/json")

    else:
        raise Http404("Bad Request")

