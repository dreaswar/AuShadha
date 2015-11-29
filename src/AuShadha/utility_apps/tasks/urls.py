from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from tasks.views import *
from tasks.dijit_widgets.pane import render_tasks_pane
from tasks.dijit_widgets.tree import render_tasks_tree

admin.autodiscover()

urlpatterns = patterns('',

                       ################################ CRUD ##################
                       url(r'tasks/list/(?P<id>\d+)/$',
                           'tasks.views.tasks_detail_list',
                           name='tasks_detail_list'
                           ),

                       url(r'tasks/add/(?P<id>\d+)/$',
                           'tasks.views.tasks_detail_add',
                           name='tasks_detail_add'
                           ),

                       url(r'tasks/edit/(?P<id>\d+)/$',
                           'tasks.views.tasks_detail_edit',
                           name='tasks_detail_edit'
                           ),

                       url(r'tasks/del/(?P<id>\d+)/$',
                           'tasks.views.tasks_detail_del',
                           name='tasks_detail_del'
                           ),

                       ################################ JSON, UI-PANE & TREE ##

                       url(r'tasks/pane/(?P<id>\d+)/$',
                           'tasks.dijit_widgets.pane.render_tasks_pane',
                           name='render_tasks_pane_with_id'
                           ),

                       url(r'tasks/pane/$',
                           'tasks.dijit_widgets.pane.render_tasks_pane',
                           name='render_tasks_pane_without_id'
                           ),

                       url(r'tasks/tree/(?P<id>\d+)/$',
                           'tasks.views.render_tasks_tree',
                           name='render_tasks_tree_with_id'
                           ),

                       url(r'tasks/tree/$',
                           'tasks.views.render_tasks_tree',
                           name='render_tasks_tree_without_id'
                           ),

                       url(r'tasks/json/$',
                           'tasks.views.render_tasks_json',
                           name='render_tasks_json_without_id'
                           ),

                       url(r'tasks/json/(?P<id>\d+)/$',
                           'tasks.views.render_tasks_json',
                           name='render_tasks_json_with_id'
                           ),

                       ################################ SUMMARY ###############

                       url(r'tasks/summary/$',
                           'tasks.views.render_tasks_summary',
                           name='render_tasks_summary_without_id'
                           ),

                       url(r'tasks/summary/(?P<id>\d+)/$',
                           'tasks.views.render_tasks_summary',
                           name='render_tasks_summary_with_id'
                           ),

                       )
