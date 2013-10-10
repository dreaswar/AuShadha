################################################################################
# Project : AuShadha
# Description: Admission Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
################################################################################

#from admission.models import AdmissionDetail

MODULE_IDENTIFIER = 'aushadha-visit'
MODULE_LABEL = 'Admission'
MODULE_TYPE = 'main_module'
PACKAGE_NAME = 'aushadha-admission'
VERSION = 0.01
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha','patient',]

ui_sections = {'app_type': 'main_module',
               'layout' : ['trailing','top','center'],
               'widgets':{ 'tree'    : '',
                           'summary' : '',
                           'grid'    : '',
                           'search'  : ''
                          }
              }