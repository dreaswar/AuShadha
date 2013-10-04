################################################################################
# Project      : AuShadha
# Description  : URLS for SocialHistory
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
################################################################################

from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings

from .views import *

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/(?P<patient_id>\d+)/$',
                      social_history_json,
                      name='social_history_json'
                      ),

                  url(r'json/$',
                      social_history_json,
                      name='social_history_json_without_id'
                      ),


                  # url(r'list/(?P<patient_id>\d+)/$',
                  #social_history_list,
                  #name = 'social_history_list'
                  #),

                  # url(r'list/$',
                  #social_history_list,
                  #name = 'social_history_list_without_id'
                  #),

                  url(r'add/(?P<patient_id>\d+)/$',
                      social_history_add,
                      name='social_history_add'
                      ),

                  url(r'add/$',
                      social_history_add,
                      name='social_history_add_without_id'
                      ),


                  url(r'edit/(?P<social_history_id>\d+)/$',
                      social_history_edit,
                      name='social_history_edit'
                      ),
                  url(r'edit/$',
                      social_history_edit,
                      name='social_history_edit_without_id'
                      ),

                  url(r'del/(?P<social_history_id>\d+)/$',
                      social_history_del,
                      name='social_history_del'
                      ),
                  url(r'del/$',
                      social_history_del,
                      name='social_history_del_without_id'
                      ),

)
