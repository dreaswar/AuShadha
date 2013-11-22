################################################################################
# Project : AuShadha
# Description: Family History Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
################################################################################

MODULE_IDENTIFIER = 'aushadha-family_history'
MODULE_LABEL = 'Family History'
MODULE_TYPE = 'sub_module'
VERSION = 0.01
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha','patient',]

ui_sections = {'app_type': 'sub_module',
               'load_after': 'patient',
               'load_first': False,
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'    : '',
                           'summary'  : '',
                           'grid'     : '',
                           'search'   : ''
                          }
              } 
