################################################################################
# Project : AuShadha
# Description: visit_prescription Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

MODULE_IDENTIFIER = 'aushadha-visit_prescription'
MODULE_LABEL = 'visit_prescription'
VERSION = 0.01
MODULE_TYPE = 'sub_module'
PARENT_MODULE = 'visit'
DEPENDS_ON = ['aushadha','patient','visit','medication_list']

ui_sections = {'app_type'  : 'sub_module',
               'load_after': 'visit',
               'load_first': False,
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'   : '',
                            'summary': '',
                            'grid'   : '',
                            'search' : ''
                          }
              }
