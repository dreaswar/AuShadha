
from django.conf.urls.defaults import *
#from django.contrib import admin
from django.conf.urls.defaults import patterns, url

import AuShadha.settings
from admission.views import *
from admission.dijit_widgets.pane import *

urlpatterns = patterns('',

                       url(r'json/$',
                           'admission.views.render_admission_json',
                           name='render_admission_json_without_id'
                           ),

                      url(r'json/(?P<patient_id>\d+)/$',
                           'admission.views.render_admission_json',
                           name='render_admission_json'
                           ),

                      url(r'pane/(?P<patient_id>\d+)/$', 
                          'admission.dijit_widgets.pane.render_admission_pane',
                          name='render_admission_pane_with_id'
                      ),

                      url(r'pane/$', 
                          'admission.dijit_widgets.pane.render_admission_pane',
                          name='render_admission_pane_without_id'
                      ),

                       #   url(r'list/(?P<id>\d+)/$',
                       #'admission.views.admission_list',
                       #name = 'get_admission_list'
                       #),

                       url(r'add/(?P<id>\d+)/$'	,
                           'admission.views.admission_add',
                           name='admission_add'
                           ),

                       url(r'add/$',
                           'admission.views.admission_add',
                           name='admission_add'
                           ),

################################ ADMISSION SUMMARY ##################################

                       url(r'summary/(?P<patient_id>\d+)/$',
                           "admission.views.admission_summary", 
                           name="admission_summary"
                           ),

                       url(r'summary/$',
                           "admission.views.admission_summary", 
                           name="admission_summary_without_id"
                           ),

################################ ADMISSION TREE ##################################

                       url(r'admission/tree/(?P<patient_id>\d+)/$',
                           'admission.views.render_admission_tree',
                           name='render_admission_tree_with_id'
                           ),

                       url(r'admission/tree/$',
                           'admission.views.render_admission_tree',
                           name='render_admission_tree_without_id'
                           ),

                       url(r'tree/(?P<patient_id>\d+)/$',
                           'admission.views.render_admission_tree',
                           name='render_admission_tree_with_id'
                           ),

                       url(r'tree/$',
                           'admission.views.render_admission_tree',
                           name='render_admission_tree_without_id'
                           )
)
