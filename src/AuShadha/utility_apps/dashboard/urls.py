from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from dashboard.views import *
from dashboard.dijit_widgets.pane import render_dashboard_pane
from dashboard.dijit_widgets.tree import render_dashboard_tree

admin.autodiscover()

urlpatterns = patterns('',

################################ CRUD ##################################
                       url(r'dashboard/list/(?P<id>\d+)/$',
                           'dashboard.views.dashboard_detail_list',
                           name='dashboard_detail_list'
                           ),

                       url(r'dashboard/add/(?P<id>\d+)/$',
                           'dashboard.views.dashboard_detail_add',
                           name='dashboard_detail_add'
                           ),

                       url(r'dashboard/edit/(?P<id>\d+)/$',
                           'dashboard.views.dashboard_detail_edit',
                           name='dashboard_detail_edit'
                           ),

                       url(r'dashboard/del/(?P<id>\d+)/$',
                           'dashboard.views.dashboard_detail_del',
                           name='dashboard_detail_del'
                           ),

################################ JSON, UI-PANE & TREE #########################

                      url(r'dashboard/pane/(?P<id>\d+)/$',
                           'dashboard.dijit_widgets.pane.render_dashboard_pane',
                           name='render_dashboard_pane_with_id'
                           ),

                      url(r'dashboard/pane/$',
                           'dashboard.dijit_widgets.pane.render_dashboard_pane',
                           name='render_dashboard_pane_without_id'
                           ),

                       url(r'dashboard/tree/(?P<id>\d+)/$',
                           'dashboard.views.render_dashboard_tree',
                           name='render_dashboard_tree_with_id'
                           ),

                       url(r'dashboard/tree/$',
                           'dashboard.views.render_dashboard_tree',
                           name='render_dashboard_tree_without_id'
                           ),

                       url(r'dashboard/json/$',
                           'dashboard.views.render_dashboard_json',
                           name='render_dashboard_json_without_id'
                           ),

                       url(r'dashboard/json/(?P<id>\d+)/$',
                           'dashboard.views.render_dashboard_json',
                           name='render_dashboard_json_with_id'
                           ),

################################ SUMMARY ###############################

                       url(r'dashboard/summary/$',
                           'dashboard.views.render_dashboard_summary',
                           name='render_dashboard_summary_without_id'
                           ),

                       url(r'dashboard/summary/(?P<id>\d+)/$',
                           'dashboard.views.render_dashboard_summary',
                           name='render_dashboard_summary_with_id'
                           ),

)
