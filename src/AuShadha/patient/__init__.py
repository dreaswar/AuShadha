################################################################################
# Project : AuShadha
# Description: Patient Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

MODULE_IDENTIFIER = 'aushadha-patient'
MODULE_LABEL = 'Patient'
VERSION = 0.01
MODULE_TYPE = 'main_module'
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha',]

ui_sections = {'app_type'  : 'main_module',
               'load_after': 'search',
               'load_first': False,
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'   : '',
                            'summary': True,
                            'grid'   : '',
                            'search' : ''
                          }
              }