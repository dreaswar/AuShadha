################################################################################
# Project : AuShadha
# Description: Patient Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

from .views import render_patient_tree
from .models import PatientDetail

MODULE_IDENTIFIER = 'aushadha-patient'
MODULE_LABEL = 'Patient'
VERSION = 0.01
MODULE_TYPE = 'main_module'
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha',]

ui_sections = {'layout' :'two_column',
               'widgets':{ 'tree':render_patient_tree,}
              }