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
#from django.core import serializers
##from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree




class AdmissionTree(object):
    """
     Defines the Dijit UI for Admission Tree
    """

    def __init__(self,request=None):
      self.request = request
      try:
        self.user = request.user
      except(AttributeError,ValueError,NameError,TypeError):
        raise Exception("Invalid User or no user supplied")

    def __unicode__(self):
      return self.__call__()

    def __call__(self):

      admission_tree_node = DijitTree()

      admission_node = DijitTreeNode({"name": "Admissions",
                                    "type": "application",
                                    "id": "ADMISSION"
                                  })

      active_admission_node = DijitTreeNode({"name": "Active Admissions",
                                            "type": "admission_module",
                                            "id": "ACTIVE_ADMISSIONS",
                                            "module_type": "sub_module",
                                            "module_name": "admission"
                                            })
      admission_node.add_child_node(active_admission_node)

      inactive_admission_node = DijitTreeNode({"name": "Previous Admissions",
                                            "type": "admission_module",
                                            "id": "PREVIOUS_ADMISSIONS",
                                            "module_type": "sub_module",
                                            "module_name": "admission"
                                            })
      admission_node.add_child_node(inactive_admission_node)
      
      admission_tree_node.add_child_node(admission_node)
      
      history_node = DijitTreeNode({"name": "History",
                                    "type": "application",
                                    "id": "HISTORY"
                                  })

      medical_history_node = DijitTreeNode({"name": "Medical History",
                                            "type": "medical_history_module",
                                            "id": "MEDICAL_HISTORY",
                                            "module_type": "sub_module",
                                            "module_name": "medical_history",
                                            "ui_layout": "standard",
                                            "widgets":['grid','button']
                                            })
      history_node.add_child_node(medical_history_node)

      surgical_history_node = DijitTreeNode({"name": "Surgical History",
                                              "type": "surgical_history_module",
                                              "id": "SURGICAL_HISTORY",
                                              "module_type": "sub_module",
                                              "module_name": "surgical_history",
                                              "ui_layout": "standard",
                                              "widgets":['grid','button']
                                            })
      history_node.add_child_node(surgical_history_node)

      family_history_node = DijitTreeNode({"name": "Family History",
                                            "type": "family_history_module",
                                            "id": "FAMILY_HISTORY",
                                            "module_type": "sub_module",
                                            "module_name": "family_history",
                                            "ui_layout": "standard",
                                            "widgets":['grid','button']
                                          })
      history_node.add_child_node(family_history_node)

      social_history_node = DijitTreeNode({"name": "Social History",
                                            "type": "social_history_module",
                                            "id": "SOCIAL_HISTORY",
                                            "module_type": "sub_module",
                                            "module_name": "social_history",
                                            "ui_layout": "standard",
                                            "widgets":['form']
                                          })
      history_node.add_child_node(social_history_node)

      contact_node = DijitTreeNode({"name": "Contact",
                                    "type": "contact_module",
                                    "id": "CONTACT",
                                    "module_type": "sub_module",
                                    "module_name": "contact",
                                    "ui_layout": "standard",
                                    "widgets":['grid','button']
                                  })
      phone_node = DijitTreeNode({"name": "Phone",
                                  "type": "phone_module",
                                  "id": "PHONE",
                                  "module_type": "sub_module",
                                  "module_name": "phone",
                                  "ui_layout": "standard",
                                  "widgets":['grid','button']
                                })
      guardian_node = DijitTreeNode({"name": "Guardian",
                                     "type": "guardian_module",
                                     "id": "GUARDIAN",
                                     "module_type": "sub_module",
                                     "module_name": "guardian",
                                     "ui_layout": "standard",
                                     "widgets":['grid','button']
                                    })

      demographics_node = DijitTreeNode({"name": "Demographics",
                                         "type": "demographics_module",
                                         "id": "DEMOGRAPHICS",
                                         "module_type": "sub_module",
                                         "module_name": "demographics",
                                         "ui_layout": "composite",
                                         "widgets":['form'],
                                         'linked_modules':[contact_node(),phone_node(),guardian_node()]
                                        })

      #demographics_node.add_child_node(contact_node)
      #demographics_node.add_child_node(phone_node)
      #demographics_node.add_child_node(guardian_node)

      history_node.add_child_node(demographics_node)

      admission_tree_node.add_child_node(history_node)

      allergy_node = DijitTreeNode({"name" : "Allergy",
                                    "type": "allergy_list_module",
                                    "module_type": "sub_module",
                                    "module_name": "allergy_list",
                                    "id" : "ALLERGY",
                                    "ui_layout": "standard",
                                    "widgets":['grid','button']
                                  })

      medication_list_node = DijitTreeNode({"name" : "Medications",
                                            "type": "application",
                                            "module_type": "medication_list_module",
                                            "module_name": "medication_list",
                                            "id" : "MEDICATIONS",
                                            "ui_layout": "composite",
                                            "widgets":['grid','button'],
                                            "linked_modules":[allergy_node()]
                                          })
      admission_tree_node.add_child_node(medication_list_node)

      preventives_node = DijitTreeNode({"name": "Preventives",
                                        "type": "application",
                                        "id": "PREVENTIVES"
                                      })

      immunisation_node = DijitTreeNode({"name": "Immunisation",
                                        "type": "immunisation_module",
                                        "id": "IMMUNISATION",
                                        "module_type": "sub_module",
                                        "module_name": "immunisation",
                                        "ui_layout": "standard",
                                        "widgets":['grid','button'],
                                        })
      preventives_node.add_child_node(immunisation_node)

      admission_tree_node.add_child_node(preventives_node)

      #medical_preventives_node = DijitTreeNode({"name": "Medical",
                                                #"type": "medical_preventives_module",
                                                #"id": "MEDICAL_PREVENTIVES"
                                                #})

      #surgical_preventives_node = DijitTreeNode({"name": "Surgical",
                                                  #"type": "surgical_preventives_module",
                                                  #"id": "SURGICAL_PREVENTIVES"
                                                #})

      #obs_and_gyn_preventives_node = DijitTreeNode({"name": "Obs & Gyn",
                                                    #"type": "obs_and_gyn_preventives_module",
                                                    #"id": "OBS_PREVENTIVES"
                                                    #})

      #admission_node = DijitTreeNode({"name" : "AdmissionDetails", 
                                      #"type" :"application", 
                                      #"id"   :"ADM"
                                      #})

      #visit_node = DijitTreeNode({"name"  : "OPD Visits", 
                                  #"type":"application", 
                                  #"id":"VISIT"
                                  #})

      investigation_node = DijitTreeNode({"name": "Investigation", 
                                          "type": "application", 
                                          "id": "INV"
                                          })
      admission_tree_node.add_child_node(investigation_node)

      imaging_node = DijitTreeNode({"name": "Imaging", 
                                    "type": "application", 
                                    "id": "IMAG"
                                    })
      admission_tree_node.add_child_node(imaging_node)

      procedure_node = DijitTreeNode({"name": "Procedures", 
                                      "type": "application", 
                                      "id": "PROCEDURES"
                                      })
      admission_tree_node.add_child_node(procedure_node)

      #calendar_node = DijitTreeNode({"name"  : "Calendar" , 
                                    #"type":"application", 
                                    #"id":"CAL" 
                                  #})

      #media_node = DijitTreeNode({"name": "Media", 
                                  #"type": "application", 
                                  #"id": "MEDIA"
                                #})

      #documents_node = DijitTreeNode({"name": "Documents",
                                      #"type": "patient_documents_module",
                                      #"id": "DOCS"
                                    #})
      #images_node = DijitTreeNode({"name": "Images",
                                    #"type": "patient_images_module",
                                    #"id": "IMAGES"
                                  #})

      #coding_node = DijitTreeNode({"name": "Coding",
                                    #"type": "application",
                                    #"id": "CODING"
                                  #})

      #icd_10_node = DijitTreeNode({"name": "ICD 10",
                                    #"type": "icd10_module",
                                    #"id": "ICD_10"
                                    #})

      #icd_10_pcs_node = DijitTreeNode({"name": "ICD 10 PC",
                                        #"type": "icd10_pcs_module",
                                        #"id": "ICD_10_PROCEDURE_CODES"
                                      #})

      jsondata = admission_tree_node.to_json()
      return json