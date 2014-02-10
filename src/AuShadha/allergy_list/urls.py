################################################################################
# Project      : AuShadha
# Description  : URLS for Allergy 
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
################################################################################

from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from allergy_list.views import *

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/(?P<patient_id>\d+)/$',
                      'allergy_list.views.allergy_list_json',
                      name='allergy_list_json'
                      ),

                  url(r'json/$',
                      'allergy_list.views.allergy_list_json',
                      name='allergy_list_json_without_id'
                      ),


                  # url(r'list/(?P<patient_id>\d+)/$',
                  #'allergy_list.views.allergy_list',
                  #name = 'allergy_list'
                  #),

                  # url(r'list/$',
                  #'allergy_list.views.allergy_list',
                  #name = 'allergy_list_without_id'
                  #),

                  url(r'add/(?P<patient_id>\d+)/$',
                      'allergy_list.views.allergy_list_add',
                      name='allergy_list_add'
                      ),

                  url(r'add/$',
                      'allergy_list.views.allergy_list_add',
                      name='allergy_list_add_without_id'
                      ),


                  url(r'edit/(?P<allergy_list_id>\d+)/$',
                      'allergy_list.views.allergy_list_edit',
                      name='allergy_list_edit'
                      ),
                  url(r'edit/$',
                      'allergy_list.views.allergy_list_edit',
                      name='allergy_list_edit_without_id'
                      ),

                  url(r'del/(?P<allergy_list_id>\d+)/$',
                      'allergy_list.views.allergy_list_del',
                      name='allergy_list_del'
                      ),
                  url(r'del/$',
                      'allergy_list.views.allergy_list_del',
                      name='allergy_list_del_without_id'
                      ),

)
