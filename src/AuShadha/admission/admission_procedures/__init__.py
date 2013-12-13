################################################################################
# Project : AuShadha
# Description: OPD Visit Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
################################################################################

from django.core.urlresolvers import reverse
#from models import VisitDetail
#from .views import render_visit_tree, render_visit_summary

MODULE_IDENTIFIER = 'aushadha-visit'
MODULE_LABEL = 'OPD Visits'
MODULE_TYPE = 'main_module'
VERSION = 0.01
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha','patient',]

ui_sections = {'app_type': 'main_module',
               'load_after': 'patient',
               'load_first': False,
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'    : '/AuShadha/visit/visit/tree/',
                           'summary'  : '',
                           'grid'     : '/AuShadha/visit/visit/json/',
                           'search'   : ''
                          }
              }