from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from patient.views import *
from patient.dijit_widgets.pane import render_patient_pane
from patient.dijit_widgets.tree import render_patient_tree

admin.autodiscover()

urlpatterns = patterns('',

                       ################################ PATIENT CRUD ##########

                       url(r'new/add/(?P<clinic_id>\d+)/$',
                           'patient.views.patient_detail_add',
                           name='patient_detail_add'
                           ),

                       url(r'new/add/$',
                           'patient.views.patient_detail_add',
                           name='patient_detail_add_without_id'
                           ),

                       url(r'patient/edit/(?P<id>\d+)/$',
                           'patient.views.patient_detail_edit',
                           name='patient_detail_edit'
                           ),
                       url(r'patient/del/(?P<id>\d+)/$',
                           'patient.views.patient_detail_del',
                           name='patient_detail_del'
                           ),


                       ################################ PATIENT JSON ##########

                       url(r'patient/json/$',
                           'patient.views.render_patient_json',
                           name='render_patient_json'
                           ),


                       ################################ PATIENT SUMMARY #######

                       url(r'patient/summary/$',
                           'patient.views.render_patient_summary',
                           name='render_patient_summary_without_id'
                           ),

                       url(r'patient/summary/(?P<patient_id>\d+)/$',
                           'patient.views.render_patient_summary',
                           name='render_patient_summary_with_id'
                           ),

                       ################################ PATIENT INFO  #########

                       url(r'patient/info/(?P<patient_id>\d+)/$',
                           'patient.views.render_patient_info',
                           name='render_patient_info'
                           ),

                       ################################ PATIENT PANE ##########

                       url(r'patient/pane/(?P<patient_id>\d+)/$',
                           'patient.dijit_widgets.pane.render_patient_pane',
                           name='render_patient_pane_with_id'
                           ),

                       url(r'patient/pane/$',
                           'patient.dijit_widgets.pane.render_patient_pane',
                           name='render_patient_pane_without_id'
                           ),

                       ################################ PATIENT TREE ##########

                       url(r'patient/tree/(?P<patient_id>\d+)/$',
                           'patient.dijit_widgets.tree.render_patient_tree',
                           name='render_patient_tree_with_id'
                           ),

                       url(r'patient/tree/$',
                           'patient.dijit_widgets.tree.render_patient_tree',
                           name='render_patient_tree_without_id'
                           ),

                       ############################ PATIENT INDEX #############

                       # url(r'patient/index/$',
                       #'patient.views.patient_index',
                       # name='patient_index'
                       #),

                       ############################ PATIENT LIST ##############

                       # url(r'patient/list/$',
                       #'patient.views.render_patient_list' ,
                       # name='render_patient_list'
                       #),

                       #    url(r'patient/list/(?P<id>\d+)/$',
                       #            'patient.views.patient_detail_list',
                       #            name = 'patient_detail_list'
                       #    ),

                       )
