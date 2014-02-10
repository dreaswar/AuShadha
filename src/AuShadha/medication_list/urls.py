################################################################################
# Project      : AuShadha
# Description  : URLS for Medication list 
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
################################################################################

from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from medication_list.views import *
from .dijit_widgets.pane import render_medication_list_pane

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/(?P<patient_id>\d+)/$',
                      'medication_list.views.medication_list_json',
                      name='medication_list_json'
                      ),

                  url(r'json/$',
                      'medication_list.views.medication_list_json',
                      name='medication_list_json_without_id'
                      ),


                  url(r'pane/(?P<patient_id>\d+)/$',
                      render_medication_list_pane,
                      name='render_medication_list_pane_with_id'
                      ),

                  url(r'pane/$',
                      render_medication_list_pane,
                      name='render_medication_list_pane_without_id'
                      ),

                  # url(r'list/(?P<patient_id>\d+)/$',
                  #'medication_list.views.medication_list',
                  #name = 'medication_list'
                  #),

                  # url(r'list/$',
                  #'medication_list.views.medication_list',
                  #name = 'medication_list_without_id'
                  #),

                  url(r'add/(?P<patient_id>\d+)/$',
                      'medication_list.views.medication_list_add',
                      name='medication_list_add'
                      ),

                  url(r'add/$',
                      'medication_list.views.medication_list_add',
                      name='medication_list_add_without_id'
                      ),


                  url(r'edit/(?P<medication_list_id>\d+)/$',
                      'medication_list.views.medication_list_edit',
                      name='medication_list_edit'
                      ),
                  url(r'edit/$',
                      'medication_list.views.medication_list_edit',
                      name='medication_list_edit_without_id'
                      ),

                  url(r'del/(?P<medication_list_id>\d+)/$',
                      'medication_list.views.medication_list_del',
                      name='medication_list_del'
                      ),
                  url(r'del/$',
                      'medication_list.views.medication_list_del',
                      name='medication_list_del_without_id'
                      ),

)
