################################################################################
# Project : AuShadha
# Description: Patient Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

#from patient.views import render_patient_tree, render_patient_summary
#from patient.models import PatientDetail
from django.core.urlresolvers import reverse

MODULE_IDENTIFIER = 'aushadha-patient'
MODULE_LABEL = 'Patient'
VERSION = 0.01
MODULE_TYPE = 'main_module'
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha',]

ui_sections = {'app_type': 'main_module',
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'   : reverse('render_patient_tree_without_id'),
                            'summary': True,
                            'grid'   : reverse('render_patient_json'),
                            'search' : True
                          }
              }