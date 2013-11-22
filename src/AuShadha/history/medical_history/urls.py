################################################################################
# Project      : AuShadha
# Description  : URLS for Medical History
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
################################################################################

from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings

from .views import *
from .dijit_widgets.pane import render_medical_history_pane

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/(?P<patient_id>\d+)/$',
                      medical_history_json,
                      name='medical_history_json'
                      ),

                  url(r'json/$',
                      medical_history_json,
                      name='medical_history_json_without_id'
                      ),

                  url(r'pane/(?P<patient_id>\d+)/$',
                      render_medical_history_pane,
                      name='render_medical_history_pane_with_id'
                      ),

                  url(r'pane/$',
                      render_medical_history_pane,
                      name='render_medical_history_pane_without_id'
                      ),

                  # url(r'list/(?P<patient_id>\d+)/$',
                  #medical_history_list,
                  #name = 'medical_history_list'
                  #),

                  # url(r'list/$',
                  #medical_history_list,
                  #name = 'medical_history_list_without_id'
                  #),

                  url(r'add/(?P<patient_id>\d+)/$',
                      medical_history_add,
                      name='medical_history_add'
                      ),

                  url(r'add/$',
                      medical_history_add,
                      name='medical_history_add_without_id'
                      ),


                  url(r'edit/(?P<medical_history_id>\d+)/$',
                      medical_history_edit,
                      name='medical_history_edit'
                      ),
                  url(r'edit/$',
                      medical_history_edit,
                      name='medical_history_edit_without_id'
                      ),

                  url(r'del/(?P<medical_history_id>\d+)/$',
                      medical_history_del,
                      name='medical_history_del'
                      ),
                  url(r'del/$',
                      medical_history_del,
                      name='medical_history_del_without_id'
                      ),

)
