################################################################################
# Project : AuShadha
# Description: Search Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
################################################################################

MODULE_LABEL = 'Search'
MODULE_IDENTIFIER = 'aushadha-search'
VERSION = 0.01
MODULE_TYPE = 'sub_module'

PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha',]

ui_sections = {'app_type' : 'sub_module',
               'layout'   : ['top','center'],
               'widgets'  : { 'tree'    : False,
                              'summary' : False,
                              'grid'    : False,
                              'search'  : True
                            }
              }