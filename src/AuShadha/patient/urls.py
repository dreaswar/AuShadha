from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings

from patient.views import *
from patient.dijit_widgets.pane import render_patient_pane

admin.autodiscover()

urlpatterns = patterns('',

############################ PATIENT CRUD ######################################

                       #url(r'patient/index/$',
                           #'patient.views.patient_index',
                           #name='patient_index'
                           #),

                       #url(r'patient/list/$',
                           #'patient.views.render_patient_list'	,
                           #name='render_patient_list'
                           #),


                       url(r'new/add/(?P<clinic_id>\d+)/$'                             ,
                           'patient.views.patient_detail_add',
                           name='patient_detail_add'
                           ),

                       url(r'new/add/$'                             ,
                           'patient.views.patient_detail_add',
                           name='patient_detail_add_without_id'
                           ),

                       #    url(r'patient/list/(?P<id>\d+)/$',
                       #            'patient.views.patient_detail_list',
                       #            name = 'patient_detail_list'
                       #    ),

                       url(r'patient/edit/(?P<id>\d+)/$',
                           'patient.views.patient_detail_edit',
                           name='patient_detail_edit'
                           ),
                       url(r'patient/del/(?P<id>\d+)/$',
                           'patient.views.patient_detail_del',
                           name='patient_detail_del'
                           ),

                      url(r'patient/info/(?P<patient_id>\d+)/$',
                           'patient.views.render_patient_info',
                           name='render_patient_info'
                           ),

                      url(r'patient/pane/(?P<patient_id>\d+)/$',
                           'patient.dijit_widgets.pane.render_patient_pane',
                           name='render_patient_pane_with_id'
                           ),

                      url(r'patient/pane/$',
                           'patient.dijit_widgets.pane.render_patient_pane',
                           name='render_patient_pane_without_id'
                           ),

################################ PATIENT TREE ##################################

                       url(r'patient/tree/(?P<patient_id>\d+)/$',
                           'patient.views.render_patient_tree',
                           name='render_patient_tree_with_id'
                           ),

                       url(r'patient/tree/$',
                           'patient.views.render_patient_tree',
                           name='render_patient_tree_without_id'
                           ),

                       url(r'patient/json/$',
                           'patient.views.render_patient_json',
                           #'patient.views.render_patient_list',
                           name='render_patient_json'
                           ),


################################ PATIENT SUMMARY ###############################

                       url(r'patient/summary/$',
                           'patient.views.render_patient_summary',
                           name='render_patient_summary_without_id'
                           ),

                       url(r'patient/summary/(?P<patient_id>\d+)/$',
                           'patient.views.render_patient_summary',
                           name='render_patient_summary_with_id'
                           ),

################################ PATIENT SIDEBAR ###############################

                       #url(r'patient/sidebar_contact_tab/$',
                           #'patient.views.render_patient_sidebar_contact_tab',
                           #name='render_patient_sidebar_contact_tab_without_id'
                           #),

                       #url(r'patient/sidebar_contact_tab/(?P<id>\d+)/$',
                           #'patient.views.render_patient_sidebar_contact_tab',
                           #name='render_patient_sidebar_contact_tab_with_id'
                           #),


######################### PATIENT SEARCH #######################################

                       url(r'patient/search/$'	,
                           'patient.views.patient_search',
                           name="patient_search"
                           ),

                      url(r'patient/search/(?P<search_by>\w+)/(?P<search_for>\w+)/$'	,
                          'patient.views.patient_search',
                          name="search_for_patient"
                         ),


                       url(r'filtering_search/$'	,
                           'patient.views.filtering_search',
                           name="filtering_search_without_id"
                           ),

                       url(r'filtering_search/(?P<id>\d+)/$'	,
                           'patient.views.filtering_search',
                           name="filtering_search_with_id"
                           ),

                       url(r'patient_id/autocompleter/$',
                           'patient.views.patient_id_autocompleter',
                           name='patient_id_autocompleter'
                           ),

                       url(r'patient_hospital_id/autocompleter/$',
                           'patient.views.hospital_id_autocompleter',
                           name='patient_hospital_id_autocompleter'
                           ),

                       url(r'patient_name/autocompleter/$'	,
                           'patient.views.patient_name_autocompleter',
                           name='patient_name_autocompleter'
                           ),

###############################################################################

                       #url(r'list/$',
                           #'patient.views.render_patient_list'  ,
                           #name='render_patient_list'
                           #),

)
