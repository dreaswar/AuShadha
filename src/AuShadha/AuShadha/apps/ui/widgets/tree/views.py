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
##from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder
#from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.settings import INSTALLED_APPS
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree

#from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
#from AuShadha.utilities.forms import aumodelformerrorformatter_factory

#from AuShadha.apps.clinic.models import Clinic
#from patient.models import PatientDetail, PatientDetailForm

#from demographics.contact.models import Contact
#from demographics.phone.models import Phone
#from demographics.guardian.models import Guardian
#from demographics.demographics.models import Demographics
#from demographics.email_and_fax.models import EmailAndFax

#from history.medical_history.models import MedicalHistory
#from history.surgical_history.models import SurgicalHistory
#from history.social_history.models import SocialHistory
#from history.family_history.models import FamilyHistory
#from history.obs_and_gyn.models import ObstetricHistoryDetail

#from allergy_list.models import Allergy
#from medication_list.models import MedicationList
#from immunisation.models import Immunisation

#from admission.models import AdmissionDetail, AdmissionDetailForm
#from visit.models import VisitDetail, VisitImaging, VisitInv



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

            jsondata = tree.to_json()
            return HttpResponse(jsondata, content_type="application/json")

    else:
        raise Http404("Bad Request")

@login_required
def visit(request, patient_id=None):
    if request.method == "GET" and request.is_ajax():
        if patient_id:
            patient_id = int(patient_id)
        else:
            try:
                patient_id = int(request.GET.get('patient_id'))
                pat_obj = PatientDetail.objects.get(pk=patient_id)
                pat_urls = pat_obj.urls
                visit_obj = VisitDetail.objects.filter(
                    patient_detail=pat_obj)
                prev_visit_obj = VisitDetail.objects.filter(
                    patient_detail=pat_obj).filter(is_active=False)
                active_visit_obj = VisitDetail.objects.filter(
                    patient_detail=pat_obj).filter(is_active=True)
            except(AttributeError, NameError, KeyError, TypeError, ValueError):
                raise Http404("ERROR! Bad Request Parameters")
            except(AttributeError, NameError, KeyError, TypeError, ValueError):
                raise Http404("ERROR! Requested Patient Data Does not exist")

            #pat_obj.generate_urls()
            #adm_obj = AdmissionDetail.objects.filter(
                #patient_detail=pat_obj)
            #demographics_obj = Demographics.objects.filter(
                #patient_detail=pat_obj)
            #social_history_obj = SocialHistory.objects.filter(
                #patient_detail=pat_obj)
            #family_history_obj = FamilyHistory.objects.filter(
                #patient_detail=pat_obj)
            #medical_history_obj = MedicalHistory.objects.filter(
                #patient_detail=pat_obj)
            #surgical_history_obj = SurgicalHistory.objects.filter(
                #patient_detail=pat_obj)
            #medication_list_obj = MedicationList.objects.filter(
                #patient_detail=pat_obj)
            #allergy_obj = Allergy.objects.filter(
                #patient_detail=pat_obj)
            #pat_inv_obj = VisitInv.objects.filter(
                #visit_detail__patient_detail=pat_obj)
            #pat_imaging_obj = VisitImaging.objects.filter(
                #visit_detail__patient_detail=pat_obj)

            tree = DijitTree()

            if pat_obj.can_add_new_visit(pat_obj):
                new_visit = DijitTreeNode({"name": "New OPD Visit",
                                          "type": "application",
                                          "id": "NEW_OPD_VISIT",
                                          "addUrl": pat_urls['add']['visit']
                                          })
                tree.add_child_node(new_visit)

            if active_visit_obj:
                active_visits = VisitDetail.objects.filter(
                    patient_detail=pat_obj).filter(is_active=True)

                active_visits_node = DijitTreeNode( {"name": "Active Visits",
                                                "type": "application",
                                                "id": "ACTIVE_VISITS",
                                                "addUrl": None,
                                                'editUrl': None,
                                                'delUrl': None
                                                })
                tree.add_child_node(active_visits_node)

                for active_visit in active_visits:
                    av_urls = active_visit.urls
                    av = DijitTreeNode({"name": active_visit.visit_date.date().isoformat(),
                                                  "type": "active_visit",
                                                  "id": "ACTIVE_VISITS_" + str(active_visit.id),
                                                  "addUrl": None,
                                                  'editUrl': av_urls['edit'],
                                                  'delUrl': av_urls['del']
                                                  })

                    av_fu = DijitTreeNode({"name": "Add Follow-Up",
                                        "type": "visit_follow_up_add",
                                        "id": "VISIT_FOLLOW_UP_ADD_" + str(active_visit.id),
                                        "addUrl": av_urls['add']['follow_up'],
                                      })
                    av.add_child_node(av_fu)
                    
                    av_orders = DijitTreeNode({"name": "Orders",
                                           "type": "application",
                                           "id": "ACTIVE_VISIT_" + str(active_visit.id) + "_ORDERS_AND_PRESCRIPTION",
                                           "addUrl": None,
                                          })
                    av.add_child_node(av_orders)
                    
                    av_close  = DijitTreeNode({"name": "Close",
                                            "type": "close_visit",
                                            "id": "VISIT_CLOSE_" + str(active_visit.id),
                                            "addUrl": active_visit.get_visit_detail_close_url(),
                                        })
                    av.add_child_node(av_close)

                    active_visits_node.add_child_node(av)

                tree.add_child_node(active_visits_node)

                    #av_edit = DijitTreeNode({"name"      : "Edit" ,
                                            #"type"       : "visit",
                                            #"id"         : "ACTIVE_VISIT_" + str(active_visit.id) ,
                                            #"addUrl"     : None,
                                            #"editUrl"    : av_urls['edit'],
                                            #"deUrl"      : av_urls['del']
                                            #})

                    #av_diagnosis = DijitTreeNode({"name"  : "Diagnosis" , 
                                                #"type":"application", 
                                                #"id":"DIAG" ,
                                                #"addUrl": None,
                                                #})

                    #av_advice = DijiTreeNode({"name"  : "Advice" , 
                                              #"type":"advice",
                                              #"id":"ADVICE" ,
                                              #"addUrl": None,
                                              #})

                    #av_procedure = DijitTreeNode({"name"  : "Procedure" , 
                                                  #"type":"procedure", 
                                                  #"id":"PROC" ,
                                                  #"addUrl": None,
                                                  #})

                    #av_calendar = DijiTreeNode({"name"  : "Calendar" , 
                                                #"type":"application", 
                                                #"id":"CAL" ,
                                                #"addUrl": None,
                                                #})

                    if active_visit.has_fu_visits():
                        fu_base = DijitTreeNode({"name": "Follow-ups",
                                                "type": "fu_visits",
                                                "id": "",
                                                "addUrl": None,
                                                "absoluteUrl": None
                                                })
                        fu_visit = active_visit.has_fu_visits()

                        for fu in fu_visit:
                            fu_node = DijitTreeNode({ "name": fu.visit_date.date().isoformat(),
                                                  "type": "fu_visit",
                                                  "id": "FU_VISIT_" + str(fu.id),
                                                  "editUrl": fu.urls['edit'],
                                                  "delUrl": fu.urls['del']
                                                })
                            fu_orders = DijitTreeNode({"name": "Orders",
                                                      "type": "application",
                                                      "id": "FU_VISIT_" + str(fu.id) + "_ORDERS_AND_PRESCRIPTION",
                                                      "addUrl": None,
                                                      })

            if prev_visit_obj:
                base_dict = {"name": "Closed Visits", "type":
                             "application", "id": "CLOSED_VISITS", 'children': []}
                sub_dict = {
                    "name": "", "type": "visit", "id": "", "editUrl": "", "delUrl": ""}
                for visit in prev_visit_obj:
                    #visit.generate_urls()
                    v_urls = visit.urls

                    prev_v = DijitTreeNode({'name': visit.visit_date.date().isoformat() + "(" + visit.op_surgeon.__unicode__() + ")",
                                            'id': "CLOSED_VISIT_" + unicode(visit.id),
                                            'absoluteUrl':visit.get_absolute_url(),
                                            'editUrl':v_urls['edit'],
                                            'delUrl': v_urls['del']})
                     
                    prev_v_orders = DijitTreeNode({"name": "Orders",
                                                  "type": "application",
                                                  "id": "CLOSED_VISIT_" + str(visit.id) + "_ORDERS_AND_PRESCRIPTION",
                                                  "len": 1,
                                                  "addUrl": None,
                                                  })

                    if visit.has_fu_visits():
                        fu_visit = visit.has_fu_visits()

                        prev_v_fu_base   = DijitTreeNode({"name": "Follow-ups",
                                        "type": "fu_visits",
                                        "id": "CLOSED_FOLLOW_UP_VISITS_" + str(visit.id),
                                        "addUrl": None,
                                        "absoluteUrl": None
                                        })

                        for fu in fu_visit:

                            prev_v_fu = DijitTreeNode({"name": fu.visit_date.date().isoformat(),
                                                       "type": "fu_visit",
                                                       "id": "CLOSED_FU_VISIT_" + str(fu.id),
                                                       "editUrl": fu.urls['edit'],
                                                       "delUrl": fu.urls['del'],
                                                      })

                            prev_v_orders = DijitTreeNode({"name": "Orders",
                                                          "type": "application",
                                                          "id": "CLOSED_FU_VISIT_" + str(fu.id) + "_ORDERS_AND_PRESCRIPTION",
                                                          "addUrl": None,
                                                          })

            procedure = DijitTreeNode({"name": "Procedures", 
                            "type": "application", 
                            "id": "PROC",
                            "addUrl": None,
                          })

            history = DijitTreeNode({"name": "History", 
                                     "type": "application", 
                                     "id": "HISTORY",
                                      "addUrl": None,
                                    })
            
            medication = DijitTreeNode({"name": "Medication", 
                                        "type": "application", 
                                        "id": "MEDICATION_LIST",
                                        "addUrl": None,
                                      })
            investigation = DijitTreeNode({"name": "Investigation", 
                                          "type": "application", 
                                          "id": "INV",
                                          "addUrl": None,
                                          })
            imaging = DijitTreeNode({"name": "Imaging", 
                                    "type": "application", 
                                    "id": "IMAG",
                                    "addUrl": None,
                                    })

            media = DijitTreeNode({"name"  : "Media" , 
                                   "type":"application", 
                                   "id":"MEDIA" ,
                                    "addUrl": None
                                  })

            documents  = DijitTreeNode({"name"  : "Documents" , 
                                        "type":"patient_documents_module", 
                                        "id":"DOCS" ,
                                        "addUrl": None,
                                        })
            media.add_child_node(documents)

            images = DijitTreeNode({"name"  : "Images" , 
                                    "type":"patient_images_module", 
                                    "id":"IMAGES" ,
                                    "addUrl": None,
                                    })
            media.add_child_node(images)


            jsondata = tree.to_json()
            return HttpResponse(jsondata, content_type="application/json")
    else:
        raise Http404("Bad Request")
