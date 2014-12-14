from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from .views import *
from .dijit_widgets.pane import render_visit_prescription_pane
from .dijit_widgets.tree import render_visit_prescription_tree

admin.autodiscover()

urlpatterns = patterns('',

################################ CRUD ##################################
                       url(r'visit_prescription/list/(?P<visit_detail_id>\d+)/$',
                           'visit.visit_prescription.views.visit_prescription_list',
                           name='visit_prescription_list'
                           ),

                       url(r'visit_prescription/add/(?P<id>\d+)/$',
                           'visit.visit_prescription.views.visit_prescription_add',
                           name='visit_prescription_add'
                           ),

                       url(r'visit_prescription/edit/(?P<id>\d+)/$',
                           'visit.visit_prescription.views.visit_prescription_edit',
                           name='visit_prescription_edit'
                           ),

                       url(r'visit_prescription/del/(?P<id>\d+)/$',
                           'visit.visit_prescription.views.visit_prescription_del',
                           name='visit_prescription_del'
                           ),

################################ JSON, UI-PANE & TREE #########################

                      url(r'visit_prescription/pane/(?P<id>\d+)/$',
                           'visit.visit_prescription.dijit_widgets.pane.render_visit_prescription_pane',
                           name='render_visit_prescription_pane_with_id'
                           ),

                      url(r'visit_prescription/pane/$',
                           'visit.visit_prescription.dijit_widgets.pane.render_visit_prescription_pane',
                           name='render_visit_prescription_pane_without_id'
                           ),

                       url(r'visit_prescription/tree/(?P<visit_detail_id>\d+)/$',
                           'visit.visit_prescription.views.render_visit_prescription_tree',
                           name='render_visit_prescription_tree_with_id'
                           ),

                       url(r'visit_prescription/tree/$',
                           'visit.visit_prescription.views.render_visit_prescription_tree',
                           name='render_visit_prescription_tree_without_id'
                           ),

                       url(r'visit_prescription/json/$',
                           'visit.visit_prescription.views.render_visit_prescription_json',
                           name='render_visit_prescription_json_without_id'
                           ),

                       url(r'visit_prescription/json/(?P<id>\d+)/$',
                           'visit.visit_prescription.views.render_visit_prescription_json',
                           name='render_visit_prescription_json_with_id'
                           ),

################################ SUMMARY ###############################

                       url(r'visit_prescription/summary/$',
                           'visit.visit_prescription.views.render_visit_prescription_summary',
                           name='render_visit_prescription_summary_without_id'
                           ),

                       url(r'visit_prescription/summary/(?P<id>\d+)/$',
                           'visit.visit_prescription.views.render_visit_prescription_summary',
                           name='render_visit_prescription_summary_with_id'
                           ),

)
