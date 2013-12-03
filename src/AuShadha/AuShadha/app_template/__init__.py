################################################################################
# Project : AuShadha
# Description: {{app_name}} Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

MODULE_IDENTIFIER = 'aushadha-{{app_name}}'
MODULE_LABEL = '{{app_name}}'
VERSION = 0.01
MODULE_TYPE = 'main_module'
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha','patient']

ui_sections = {'app_type'  : 'main_module',
               'load_after': 'patient',
               'load_first': False,
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'   : '',
                            'summary': '',
                            'grid'   : '',
                            'search' : ''
                          }
              }