################################################################################
# Project : AuShadha
# Description: Search Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
################################################################################

from django.core.urlresolvers import reverse

MODULE_LABEL = 'Search'
MODULE_IDENTIFIER = 'aushadha-search'
VERSION = 0.01
MODULE_TYPE = 'sub_module'

PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha',]

ui_sections = {'app_type' : 'main_module',
               'layout'   : ['top','center'],
               'load_first': True,
               'load_after': 'first',
               'widgets'  : { 'tree'   : False,
                              'summary': False,
                              'grid'   : False,
                              'search' : "/AuShadha/search/patient/",
                              'pane': "/AuShadha/search/pane/"
                            }
              }