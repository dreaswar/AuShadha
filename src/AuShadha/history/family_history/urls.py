##########################################################################
# Project      : AuShadha
# Description  : URLS for Family History
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
##########################################################################

from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from .views import *
from .dijit_widgets.pane import render_family_history_pane

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'json/(?P<patient_id>\d+)/$',
                           family_history_json,
                           name="family_history_json"
                           ),

                       url(r'json/$',
                           family_history_json,
                           name="family_history_json_without_id"
                           ),

                       url(r'pane/(?P<patient_id>\d+)/$',
                           render_family_history_pane,
                           name="render_family_history_pane_with_id"
                           ),

                       url(r'pane/$',
                           render_family_history_pane,
                           name="render_family_history_pane_without_id"
                           ),


                       # url(r'list/(?P<patient_id>\d+)/$',
                       # family_history_list,
                       #name = "family_history_list"
                       #),

                       # url(r'list/$',
                       # family_history_list,
                       #name = "family_history_list_without_id"
                       #),

                       url(r'add/(?P<patient_id>\d+)/$',
                           family_history_add,
                           name="family_history_add"
                           ),

                       url(r'add/$',
                           family_history_add,
                           name="family_history_add_without_id"
                           ),


                       url(r'edit/(?P<family_history_id>\d+)/$',
                           family_history_edit,
                           name="family_history_edit"
                           ),
                       url(r'edit/$',
                           family_history_edit,
                           name="family_history_edit_without_id"
                           ),

                       url(r'del/(?P<family_history_id>\d+)/$',
                           family_history_del,
                           name="family_history_del"
                           ),
                       url(r'del/$',
                           family_history_del,
                           name="family_history_del_without_id"
                           ),

                       )
