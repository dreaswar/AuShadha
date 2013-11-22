################################################################################
# Project      : AuShadha
# Description  : URLS for Immunisation History
# Author       : Dr. Easwar T.R
# Date         : 21-09-2013
# License      : GNU-GPL Version 3, see AuShadha/LICENSE.txt
################################################################################

from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings

from immunisation.views import *
from .dijit_widgets.pane import render_immunisation_pane

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/(?P<patient_id>\d+)/$',
                      'immunisation.views.immunisation_json',
                      name='immunisation_json'
                      ),

                  url(r'json/$',
                      'immunisation.views.immunisation_json',
                      name='immunisation_json_without_id'
                      ),

                  url(r'pane/(?P<patient_id>\d+)/$',
                      render_immunisation_pane,
                      name='render_immunisation_pane_with_id'
                      ),

                  url(r'pane/$',
                      render_immunisation_pane,
                      name='render_immunisation_pane_without_id'
                      ),

                  # url(r'list/(?P<patient_id>\d+)/$',
                  #'immunisation.views.immunisation_list',
                  #name = 'immunisation_list'
                  #),

                  # url(r'list/$',
                  #'immunisation.views.immunisation_list',
                  #name = 'immunisation_list_without_id'
                  #),

                  url(r'add/(?P<patient_id>\d+)/$',
                      'immunisation.views.immunisation_add',
                      name='immunisation_add'
                      ),

                  url(r'add/$',
                      'immunisation.views.immunisation_add',
                      name='immunisation_add_without_id'
                      ),


                  url(r'edit/(?P<immunisation_id>\d+)/$',
                      'immunisation.views.immunisation_edit',
                      name='immunisation_edit'
                      ),
                  url(r'edit/$',
                      'immunisation.views.immunisation_edit',
                      name='immunisation_edit_without_id'
                      ),

                  url(r'del/(?P<immunisation_id>\d+)/$',
                      'immunisation.views.immunisation_del',
                      name='immunisation_del'
                      ),
                  url(r'del/$',
                      'immunisation.views.immunisation_del',
                      name='immunisation_del_without_id'
                      ),

)
