################################################################################
# Project      : AuShadha
# Description  : URLS for Surgical History
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
################################################################################

from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings

from surgical_history.views import *

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/(?P<patient_id>\d+)/$',
                      'surgical_history.views.surgical_history_json',
                      name='surgical_history_json'
                      ),

                  url(r'json/$',
                      'surgical_history.views.surgical_history_json',
                      name='surgical_history_json_without_id'
                      ),


                  # url(r'list/(?P<patient_id>\d+)/$',
                  #'surgical_history.views.surgical_history_list',
                  #name = 'surgical_history_list'
                  #),

                  # url(r'list/$',
                  #'surgical_history.views.surgical_history_list',
                  #name = 'surgical_history_list_without_id'
                  #),

                  url(r'add/(?P<patient_id>\d+)/$',
                      'surgical_history.views.surgical_history_add',
                      name='surgical_history_add'
                      ),

                  url(r'add/$',
                      'surgical_history.views.surgical_history_add',
                      name='surgical_history_add_without_id'
                      ),


                  url(r'edit/(?P<surgical_history_id>\d+)/$',
                      'surgical_history.views.surgical_history_edit',
                      name='surgical_history_edit'
                      ),
                  url(r'edit/$',
                      'surgical_history.views.surgical_history_edit',
                      name='surgical_history_edit_without_id'
                      ),

                  url(r'del/(?P<surgical_history_id>\d+)/$',
                      'surgical_history.views.surgical_history_del',
                      name='surgical_history_del'
                      ),
                  url(r'del/$',
                      'surgical_history.views.surgical_history_del',
                      name='surgical_history_del_without_id'
                      ),

)
